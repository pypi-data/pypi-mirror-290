

<script>
///
//
import { verify_signature } from './verify_signature'
//
import Barcode_Vision from '$lib/trinkets/Barcode/Vision/Trinket.svelte'
//
import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'
//
import { ConicGradient } from '@skeletonlabs/skeleton';
import * as AptosSDK from "@aptos-labs/ts-sdk";
//
import { onMount, onDestroy } from 'svelte';
import { Html5QrcodeScanner, Html5QrcodeScanType, Html5Qrcode } from "html5-qrcode";
//
//
//\

import { 
	refresh_truck, 
	retrieve_truck, 
	monitor_truck 
} from '$lib/Friends_Moves/AA_Transfer_G1/Friends_Panel/Logistics/Truck'
let prepared = "no"
let Truck_Monitor;
let freight;
onMount (async () => {
	const Truck = retrieve_truck ()
	freight = Truck.freight; 
	
	prepared = "yes"
});
onDestroy (() => {
	
});


/*
	

*/
let scanned = "no"
let barcode_vision = ""
const on_barcode_found = async ({ hexadecimal_string }) => {
	console.log ('barcode found!')
	if (scanned === "no") {
		scanned = "yes"
	}
	else {
		return
	}
	
	freight.transaction_signature.hexadecimal_string = hexadecimal_string	
	const transaction_signature_Aptos_object = AptosSDK.AccountAuthenticator.deserialize (
		new AptosSDK.Deserializer (
			Uint8Array_from_string (
				freight.transaction_signature.hexadecimal_string
			)
		)
	);
	freight.transaction_signature.Aptos_object = transaction_signature_Aptos_object
	freight.transaction_signature.Aptos_object_fiberized = transaction_signature_Aptos_object
	
	verify_signature ({ freight })
}

const on_scan_error = () => {
	// console.log ('on_error')
}




</script>

<div>
	<div
		style="
			text-align: center;
			padding: .2cm 0;
		"
	>
		<header
			style="
				text-align: center;
				font-size: 1.5em;
				padding: .2cm 0;
			"
		>QR Barcode Camera</header>
		<p>
			<span>After signing the transaction at </span>
			<a 
				target="_blank"
				href="/relatives/signatures"
			>
				/relatives/signatures
			</a>
		</p>
		<p>a picture of the signed transaction QR barcode can be recorded here.</p>
		
		<div style="height: 8px"></div>
		
	</div>

	<Barcode_Vision
		bind:this={ barcode_vision }
		found={ on_barcode_found }
	/>
</div>