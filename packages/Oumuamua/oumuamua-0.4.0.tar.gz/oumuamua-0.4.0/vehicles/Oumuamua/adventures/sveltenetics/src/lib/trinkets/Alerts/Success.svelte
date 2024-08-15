



<script>


/*
import Alert_Success from '$lib/trinkets/Alerts/Success.svelte'
<Alert_Success 
	text={}
/>
*/




export let text;


</script>

{#if typeof text === "string" && text.length >= 1}
<aside 
	class="alert variant-filled-success" 
	style="
		position: relative;
	
		display: flex; 
		flex-direction: row;
		align-items: center;
		
		padding: 12px; 
		margin-top: 8px
	"
>
	<div 
		class="alert-message" 
		style="
			padding: 0 0 0 10px; 
			margin: 0;
			text-align: center;
		"
	>
		<p>{ text }</p>
	</div>
</aside>
{/if}