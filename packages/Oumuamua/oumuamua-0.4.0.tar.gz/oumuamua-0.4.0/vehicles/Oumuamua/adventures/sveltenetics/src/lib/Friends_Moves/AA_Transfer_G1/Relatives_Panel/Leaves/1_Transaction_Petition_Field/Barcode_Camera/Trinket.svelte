

<script>

///
//
import { TabGroup, Tab, TabAnchor } from '@skeletonlabs/skeleton';
import { ConicGradient } from '@skeletonlabs/skeleton';
import { onMount, onDestroy } from 'svelte';
import { Html5QrcodeScanner, Html5QrcodeScanType, Html5Qrcode } from "html5-qrcode";
//
import { 
	build_unsigned_tx_from_hexadecimal_string 
} from '$lib/PTO/Transaction/Unsigned/from_hexadecimal_string'

import { add_unsigned_transaction } from '../Screenplays/add_unsigned_transaction'

import UT_Stringified from '$lib/PTO/Transaction/Unsigned/Stringified.svelte'
//
//\
import Barcode_Vision from '$lib/trinkets/Barcode/Vision/Trinket.svelte'
	
	
let barcode_vision = ""
const found = async (packet) => {
	const { hexadecimal_string } = packet;
	
	console.log ('A barcode was found!')
	if (freight.Unsigned_Transaction_Fields.camera.searching === "yes") {
		freight.Unsigned_Transaction_Fields.camera.searching = "no"
	}
	else {
		return
	}
	
	await add_unsigned_transaction ({
		unsigned_transaction_hexadecimal_string: hexadecimal_string,
		freight
	})
	
	freight.Unsigned_Transaction_Fields.camera.barcode_found = "yes"
	freight.Unsigned_Transaction_Fields.info_text = ""
	freight.Unsigned_Transaction_Fields.alert_success = "The barcode was scanned and the unsigned transaction object built."
}
	
	



import { 
	refresh_truck, 
	retrieve_truck, 
	monitor_truck,
	verify_land
} from '$lib/Friends_Moves/AA_Transfer_G1/Relatives_Panel/Logistics/Truck'
let prepared = "no"
let Truck_Monitor;
let freight;
onMount (async () => {
	const Truck = retrieve_truck ()
	freight = Truck.freight; 
		
	Truck_Monitor = monitor_truck ((_freight) => {
		freight = _freight;
	})
	
	prepared = "yes"
});
onDestroy (() => {
	Truck_Monitor.stop ()
});





</script>


<div>
	<div style="padding: 5px 0 10px;">
		<header
			style="
				text-align: center;
				font-size: 1.4em;
				padding: .2cm 0;
			"
		>QR Barcode Camera</header>
		<p
			style="
				text-align: center;
			"
		>The "Request Camera Permissions" button opens the barcode scan.</p>
		<p
			style="
				text-align: center;
			"
		>If there's a problem with the scan, maybe try refreshing the browser and checking if the camera is connected and on.</p>
	</div>

	<Barcode_Vision
		bind:this={ barcode_vision }
		found={ found }
	/>
</div>
