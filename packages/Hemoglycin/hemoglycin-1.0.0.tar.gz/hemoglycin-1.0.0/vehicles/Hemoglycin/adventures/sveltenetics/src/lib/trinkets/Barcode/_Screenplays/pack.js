

import pako from 'pako';

export const pack_string = (the_string) => {
	// converts string to a Uint8Array (binary format)
	const string_as_Uint8Array = new TextEncoder ().encode (the_string);

	// Compress the binary data using pako
	const packed = pako.deflate (string_as_Uint8Array);

	// Convert compressed binary data to a base64 string for easier handling
	return btoa (String.fromCharCode (...new Uint8Array (packed)));
}
