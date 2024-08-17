




/*
	import { make_barcode } from '$lib/Barcode/make'
	make_barcode ({
		barcode_element,
		hexadecimal_string: ""
	})
*/

/*
	https://www.npmjs.com/package/pako
*/


import { BrowserQRCodeSvgWriter } from '@zxing/browser';
import pako from 'pako';
import bwipjs from 'bwip-js';

import { pack_string } from '../_Screenplays/pack'
import { unpack_string } from '../_Screenplays/unpack'

import { make_with_zxing } from './make_with_zxing'
import { make_with_bwip } from './make_with_bwip'


export const make_barcode = ({
	barcode_element, 
	hexadecimal_string,
	size = 500
}) => {
	
	const packed_hexadecimal_string = pack_string (hexadecimal_string)
	const unpacked_hexadecimal_string = unpack_string (packed_hexadecimal_string)
	const equal = unpacked_hexadecimal_string === hexadecimal_string;
	
	if (equal !== true) {
		console.error ({
			equal,
			unpacked_hexadecimal_string,
			hexadecimal_string,
			packed_hexadecimal_string,
			"packed_hexadecimal_string length": packed_hexadecimal_string.length,
			"hexadecimal_string length": hexadecimal_string.length
		})
		
		throw new Error ("The bytecode packing failed.")
	}
	
	/*
	make_with_bwip ({
		barcode_element, 
		packed_hexadecimal_string,
		size
	})
	*/
	
	make_with_zxing ({
		barcode_element, 
		packed_hexadecimal_string,
		size
	})
	
	return;
}

