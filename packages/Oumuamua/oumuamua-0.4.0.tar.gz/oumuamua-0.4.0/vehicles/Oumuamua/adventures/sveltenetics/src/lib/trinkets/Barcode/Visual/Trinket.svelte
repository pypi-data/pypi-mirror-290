








<script>

/*
	import Barcode_Visual from '$lib/trinkets/Barcode/Visual/Trinket.svelte'
	<Barcode_Visual 
		hexadecimal_string={ }
	/>
*/

/*
	https://www.npmjs.com/package/html5-qrcode
*/

///
//
import { make_barcode } from './make'
//
import { onMount, onDestroy } from 'svelte';
//
//\


export let hexadecimal_string = ""
$: {
	let _hexadecimal_string = hexadecimal_string;
	make ()
}

let barcode_element = ""

const make = () => {
	if (
		typeof hexadecimal_string === 'string' && 
		hexadecimal_string.length >= 1 &&
		prepared === "yes"
	) {
		make_barcode ({
			barcode_element,
			hexadecimal_string,
			size: 400
		})
	}
}

let prepared = "no"
onMount (() => {
	prepared = "yes"
	
	setTimeout (() => {
		make ()
	}, 1000)
});



</script>



<div class="card variant-filled-surface">		
	<div
		style="
			max-width: 500px;
			margin: 0 auto;
			padding: 20px;
		"
	>
		<div 
			bind:this={ barcode_element }
			style=""
		></div>
	</div>
</div>