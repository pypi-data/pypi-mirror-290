




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


/*
	<pre
		style="
			display: flex;
			justify-content: center;
		"
	>
		<code 
			id="result" 
			bind:this={ barcode_element }
		></code>
	</pre>
*/
const make_with_zxing = ({
	barcode_element,
	packed_hexadecimal_string,
	size
}) => {
	const code_writer = new BrowserQRCodeSvgWriter ()
	
	code_writer.writeToDom (
		barcode_element, 
		// hexadecimal_string,
		packed_hexadecimal_string,

		size, 
		size
	)
}


/*
	barcode: [ 'azteccode', 'Aztec Code' ],
	barcode_options: [
		[ 'qrcode', 'QR Code' ],
		[ 'azteccode', 'Aztec Code' ]
	]
	
	<canvas 
		id="result" 
		bind:this={ barcode_element }
		
		style=""
	></canvas>
*/
const make_with_bwip = ({
	barcode_element,
	packed_hexadecimal_string,
	size
}) => {
	const canvas = barcode_element;
	
	const palette = '000000'
	
	// [ 'qrcode', 'QR Code' ],
	// [ 'azteccode', 'Aztec Code' ],
	
	const SVG = bwipjs.toSVG ({
		bcid: 'qrcode',
		
		text: packed_hexadecimal_string,
		
		scale: 3,
		height: 29,
		
		includetext: true,
		textxalign: 'center',

		barcolor: palette, 
		bordercolor: palette,
		textcolor: palette 
	});
	
	console.log ({ SVG })
	
	barcode_element.innerHTML = SVG;
}

export const make_barcode = ({
	barcode_element, 
	hexadecimal_string,
	size = 500
}) => {
	const code_writer = new BrowserQRCodeSvgWriter ()
	
	// console.log ({ code_writer })
	
	if (true) {
		// let string = new Uint8Array ([ 255, 255 ])
		
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
		}

		make_with_bwip ({
			barcode_element, 
			packed_hexadecimal_string,
			size
		})
		return;

		make_with_zxing ({
			barcode_element, 
			packed_hexadecimal_string,
			size
		})
		
		return;
	}

}

