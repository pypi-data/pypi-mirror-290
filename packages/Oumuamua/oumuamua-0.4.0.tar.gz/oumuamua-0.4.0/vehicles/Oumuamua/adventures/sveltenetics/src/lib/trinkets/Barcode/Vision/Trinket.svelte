

<script>

/*
	import Barcode_Vision from '$lib/trinkets/Barcode_Vision/Trinket.svelte'
	
	const found = () => {}
	
	<Barcode_Vision
		bind:this={ barcode_vision }
		found={ found }
	/>
*/

/*
	todo:
		ask for camera permission:
			"Permit Vision"
			
		Code:
			Aztec
			QR
*/

/*
	https://scanapp.org/html5-qrcode-docs/docs/intro
	https://www.npmjs.com/package/html5-qrcode
*/

///
//
import { TabGroup, Tab, TabAnchor } from '@skeletonlabs/skeleton';
import { ConicGradient } from '@skeletonlabs/skeleton';
import { onMount, onDestroy } from 'svelte';
import { Html5QrcodeScanner, Html5QrcodeScanType, Html5Qrcode, Html5QrcodeSupportedFormats } from "html5-qrcode";
//
//\

import { unpack_string } from '../_Screenplays/unpack'


export let found = () => {}

let can_scan = "yes"
const stop = () => {
	can_scan = "no"
}

const on_camera_success = async (decodedText, decodedResult) => {
	if (can_scan !== "yes") {
		return;
	}
	
	const hexadecimal_string = unpack_string (decodedText)
	
	found ({
		hexadecimal_string,
		
		decodedText,
		decodedResult
	})
}

const on_camera_error = function () {
	console.log ('on_error', arguments)
}

let HTML5_QR_Barcode_Scanner;

const open_camera = () => {
	/*
	Html5Qrcode.
	getCameras ().
	then (devices => {
		console.log ({ devices })
		
		if (devices && devices.length) {
			var cameraId = devices [0].id;
			// .. use this to start scanning.
		}
	}).
	catch (err => {
		console.error (err)
	});

	const formatsToSupport = [
		Html5QrcodeSupportedFormats.QR_CODE,
		Html5QrcodeSupportedFormats.UPC_A,
		Html5QrcodeSupportedFormats.UPC_E,
		Html5QrcodeSupportedFormats.UPC_EAN_EXTENSION,
	];
	*/
	
	const config = {
		fps: 10,
		qrbox: {
			width: 500, 
			height: 500
		},
		formatsToSupport: [
			Html5QrcodeSupportedFormats.QR_CODE,
			Html5QrcodeSupportedFormats.AZTEC			
		],
		
		// rememberLastUsedCamera: true,
		// Only support camera scan type.
		// supportedScanTypes: [ Html5QrcodeScanType.SCAN_TYPE_CAMERA ]
	}
	
	if (true) {
		HTML5_QR_Barcode_Scanner = new Html5QrcodeScanner (
			"barcode_visuals", 
			config, 
			/* verbose= */ false
		);
		
		console.info ({ HTML5_QR_Barcode_Scanner })
		

		HTML5_QR_Barcode_Scanner.render (
			on_camera_success,
			on_camera_error
		);
		
		console.info ({ HTML5_QR_Barcode_Scanner })
	}
	
	if (false) {
		let HTML5_QR_Barcode_Scanner = new Html5QrcodeScanner (
			"barcode_visuals", 
			config, 
			/* verbose= */ false
		);
		
		
		
		//
		// facingMode [ "environment", "user" ]
		//
		//
		HTML5_QR_Barcode_Scanner.start (
			{ 
				facingMode: "environment" 
			}, 
			config, 
			on_camera_success,
			on_camera_error
		);
	}
	
	
}

const stop_the_scan = () => {
	console.info ("stop_the_scan")
	
	if (HTML5_QR_Barcode_Scanner) {
		console.info ("stopping")
		
		HTML5_QR_Barcode_Scanner.pause ()		
		// HTML5_QR_Barcode_Scanner.clear ()
	}
}

let prepared = "no"
onMount (async () => {
	open_camera ();
	prepared = "yes"
});

onDestroy (async () => {
	if (HTML5_QR_Barcode_Scanner) {
		try {
			HTML5_QR_Barcode_Scanner.clear ()
		}
		catch (exception) {
			console.error (exception)
		}
	}
})

</script>


<div>
	<div 
		id='barcode_visuals'
		style="
			height: 400px; 
			width: 100%; 
			max-width: 600px; 
			margin: 0 auto;
		"
	></div>
	
	<button 
		style="
			display: none;
		"
	
		type="button" 
		class="btn variant-filled"
		
		on:click={ stop_the_scan }
	>Stop The Scan</button>
</div>
