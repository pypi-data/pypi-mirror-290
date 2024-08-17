
import pako from 'pako';


// Decompress the base64-encoded compressed string
export const unpack_string = (base64String) => {
    // Convert base64 string to binary string
    const binaryString = atob (base64String);

    // Convert binary string to Uint8Array
    const binaryLen = binaryString.length;
    const bytes = new Uint8Array(binaryLen);
    for (let i = 0; i < binaryLen; i++) {
        bytes[i] = binaryString.charCodeAt(i);
    }

    // Decompress the Uint8Array using pako
    const decompressed = pako.inflate(bytes, { to: 'string' });

    return decompressed;
}