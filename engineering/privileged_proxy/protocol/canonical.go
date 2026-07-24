package protocol

import (
	"bytes"
	"encoding/json"
	"errors"
	"io"
	"regexp"
	"sort"
	"unicode/utf8"
)

var canonicalInteger = regexp.MustCompile(`^-?(0|[1-9][0-9]*)$`)

type scanLimits struct {
	maxBytes      int
	maxCollection int
	maxDepth      int
	maxString     int
}

func requestLimits() scanLimits {
	return scanLimits{
		maxBytes:      MaximumRequestBytes,
		maxCollection: MaximumCollectionEntries,
		maxDepth:      MaximumNestingDepth,
		maxString:     MaximumStringBytes,
	}
}

// DecodeRequest requires the input itself to be canonical. It rejects duplicates,
// unknown fields, trailing data, non-integer numbers, non-ASCII protocol strings,
// excessive nesting, and oversized collections before returning a model.
func DecodeRequest(data []byte) (RequestEnvelope, *Failure) {
	var zero RequestEnvelope
	if len(data) > MaximumRequestBytes {
		return zero, Fail(ReasonRequestOversized, SafeMessage(ReasonRequestOversized))
	}
	if !utf8.Valid(data) || bytes.HasPrefix(data, []byte{0xef, 0xbb, 0xbf}) {
		return zero, Fail(ReasonRequestMalformed, SafeMessage(ReasonRequestMalformed))
	}
	if failure := scanJSON(data, requestLimits()); failure != nil {
		return zero, failure
	}
	decoder := json.NewDecoder(bytes.NewReader(data))
	decoder.DisallowUnknownFields()
	decoder.UseNumber()
	var request RequestEnvelope
	if err := decoder.Decode(&request); err != nil {
		if bytes.Contains([]byte(err.Error()), []byte("unknown field")) {
			return zero, Fail(ReasonUnknownField, SafeMessage(ReasonUnknownField))
		}
		return zero, Fail(ReasonRequestMalformed, SafeMessage(ReasonRequestMalformed))
	}
	if err := requireEOF(decoder); err != nil {
		return zero, Fail(ReasonRequestMalformed, SafeMessage(ReasonRequestMalformed))
	}
	canonical, failure := EncodeCanonical(request, MaximumRequestBytes)
	if failure != nil || !bytes.Equal(canonical, data) {
		return zero, Fail(ReasonRequestMalformed, "Request must use canonical JSON.")
	}
	return request, nil
}

func EncodeCanonical(value any, maximum int) ([]byte, *Failure) {
	data, err := json.Marshal(value)
	if err != nil {
		return nil, Fail(ReasonInternalFailClosed, "Canonical serialization failed.")
	}
	if len(data) > maximum {
		reason := ReasonResponseOversized
		if maximum == MaximumRequestBytes {
			reason = ReasonRequestOversized
		}
		return nil, Fail(reason, SafeMessage(reason))
	}
	if !utf8.Valid(data) {
		return nil, Fail(ReasonInternalFailClosed, "Canonical serialization was not UTF-8.")
	}
	return data, nil
}

func scanJSON(data []byte, limits scanLimits) *Failure {
	if len(data) > limits.maxBytes {
		return Fail(ReasonRequestOversized, SafeMessage(ReasonRequestOversized))
	}
	decoder := json.NewDecoder(bytes.NewReader(data))
	decoder.UseNumber()
	if failure := scanValue(decoder, 0, limits); failure != nil {
		return failure
	}
	if err := requireEOF(decoder); err != nil {
		return Fail(ReasonRequestMalformed, SafeMessage(ReasonRequestMalformed))
	}
	return nil
}

func scanValue(decoder *json.Decoder, depth int, limits scanLimits) *Failure {
	if depth > limits.maxDepth {
		return Fail(ReasonRequestMalformed, "JSON nesting exceeds the governed limit.")
	}
	token, err := decoder.Token()
	if err != nil {
		return Fail(ReasonRequestMalformed, SafeMessage(ReasonRequestMalformed))
	}
	switch value := token.(type) {
	case json.Delim:
		switch value {
		case '{':
			seen := make(map[string]struct{})
			keys := make([]string, 0)
			for decoder.More() {
				keyToken, keyErr := decoder.Token()
				if keyErr != nil {
					return Fail(ReasonRequestMalformed, SafeMessage(ReasonRequestMalformed))
				}
				key, ok := keyToken.(string)
				if !ok || key == "" || !validASCII(key, limits.maxString) {
					return Fail(ReasonRequestMalformed, "Object field name is invalid.")
				}
				if _, exists := seen[key]; exists {
					return Fail(ReasonDuplicateField, SafeMessage(ReasonDuplicateField))
				}
				seen[key] = struct{}{}
				keys = append(keys, key)
				if len(keys) > limits.maxCollection {
					return Fail(ReasonRequestMalformed, "Object exceeds the governed field limit.")
				}
				if failure := scanValue(decoder, depth+1, limits); failure != nil {
					return failure
				}
			}
			if _, closeErr := decoder.Token(); closeErr != nil {
				return Fail(ReasonRequestMalformed, SafeMessage(ReasonRequestMalformed))
			}
			if !sort.StringsAreSorted(keys) {
				return Fail(ReasonRequestMalformed, "Object fields are not in canonical order.")
			}
		case '[':
			count := 0
			for decoder.More() {
				count++
				if count > limits.maxCollection {
					return Fail(ReasonRequestMalformed, "Array exceeds the governed entry limit.")
				}
				if failure := scanValue(decoder, depth+1, limits); failure != nil {
					return failure
				}
			}
			if _, closeErr := decoder.Token(); closeErr != nil {
				return Fail(ReasonRequestMalformed, SafeMessage(ReasonRequestMalformed))
			}
		default:
			return Fail(ReasonRequestMalformed, SafeMessage(ReasonRequestMalformed))
		}
	case string:
		if !validASCII(value, limits.maxString) {
			return Fail(ReasonRequestMalformed, "Protocol strings must be bounded canonical ASCII.")
		}
	case json.Number:
		if !canonicalInteger.MatchString(string(value)) || value == "-0" {
			return Fail(ReasonRequestMalformed, "Only canonical integer numbers are accepted.")
		}
	case bool:
		return nil
	case nil:
		return Fail(ReasonRequestMalformed, "Null values are not accepted by protocol v1.")
	default:
		return Fail(ReasonRequestMalformed, SafeMessage(ReasonRequestMalformed))
	}
	return nil
}

func validASCII(value string, maximum int) bool {
	if len(value) > maximum {
		return false
	}
	for _, char := range []byte(value) {
		if char < 0x20 || char > 0x7e {
			return false
		}
	}
	return true
}

// ValidateCanonicalJSON applies the bounded lexical rules to repository security
// state before a package performs strict typed decoding.
func ValidateCanonicalJSON(data []byte, maximum int) *Failure {
	limits := requestLimits()
	limits.maxBytes = maximum
	return scanJSON(data, limits)
}

func requireEOF(decoder *json.Decoder) error {
	var extra any
	err := decoder.Decode(&extra)
	if errors.Is(err, io.EOF) {
		return nil
	}
	if err == nil {
		return errors.New("trailing JSON value")
	}
	return err
}
