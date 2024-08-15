






<script>

import Panel from '$lib/trinkets/panel/trinket.svelte'

import { AppRail, AppRailTile, AppRailAnchor } from '@skeletonlabs/skeleton';
import { parse_styles } from '$lib/trinkets/styles/parse'

const trends = {
	panel: {
		position: 'relative',
		display: 'inline-flex',
		'width': '32%', 
		'height': '150px',
		'align-items': 'center',
		'justify-content': 'center',
		
		'box-sizing': 'border-box'
	},
	anchor: parse_styles ({
		position: 'absolute',
		height: '100%',
		width: '100%',
		
		display: 'flex',
		'align-items': 'center',
		'justify-content': 'center',
		'text-decoration': 'none',
		'text-align': 'center',
		'font-size': '2em'
	})
}

</script>

<style>

@media (max-width: 600px) {
    .latest-block-panel {
		flex-direction: column !important;
	}
}
a {
	line-height: 110%;
}

</style>

<svelte:head>
	<title>Technicians, Plays</title>
	<meta name="description" content="Technicians" />
</svelte:head>


<div>
	<div 
		style="padding: 25px 0"
		class="text-column"
	>
		<h1>Technicians</h1>
		
		<div style="height: 20px"></div>
		<p 
			style="text-align: center"
		>This region is for verifying and ensuring the health and continuity of the dapp.</p>
		<p
			style="text-align: center"
		>It's status checks that don't have an impact on the rest of the dapp.</p>
	</div>


	<section
		styles={{
			position: 'relative',
			display: 'grid',
			'width': '100%'
		}}
	>
		<Panel 
			styles={ trends.panel }
		>
			<a 
				class="anchor" 
				href="/Technicians/Net_Choices_with_Text"
				style="{ trends.anchor }"
			>
				Nets Choices with Text
			</a>
		</Panel>
	
		<Panel 
			styles={ trends.panel }
		>
			<a 
				class="anchor" 
				href="/Technicians/Amount_Field"
				style="{ trends.anchor }"
			>
				Amount Field
			</a>
		</Panel>
		
		<Panel 
			styles={ trends.panel }
		>
			<a 
				class="anchor" 
				href="/Technicians/Hone_Focus"
				style="{ trends.anchor }"
			>
				Hone Focus
			</a>
		</Panel>
		
		
		
		<hr 
			class="!border-t-4"
			style="margin: 4px 0 12px"
		>
		
		<Panel 
			styles={ trends.panel }
		>
			<a 
				class="anchor" 
				href="/Technicians/Address_Qualities"
				style="{ trends.anchor }"
			>
				Address Qualities with Address
			</a>
		</Panel>
		
		<Panel 
			styles={ trends.panel }
		>
			<a 
				class="anchor" 
				href="/Technicians/Address_Qualities"
				style="{ trends.anchor }"
			>
				Address Qualities
			</a>
		</Panel>
		
		<Panel 
			styles={ trends.panel }
		>
			<a 
				class="anchor" 
				href="/Technicians/Nets_Choices"
				style="{ trends.anchor }"
			>
				Nets Choices
			</a>
		</Panel>
		
		

		
		<Panel 
			styles={ trends.panel }
		>
			<a 
				class="anchor" 
				href="/Technicians/Consensus_Transactions"
				style="{ trends.anchor }"
			>
				Consensus Transactions
			</a>
		</Panel>
		<Panel 
			styles={ trends.panel }
		>
			<a 
				class="anchor" 
				href="/Technicians/Polytope"
				style="{ trends.anchor }"
			>
				Polytope
			</a>
		</Panel>
		
		<hr 
			class="!border-t-4"
			style="margin: 4px 0 12px"
		>
	</section>
	
	<Panel styles={{
		'margin': '4px',
		'width': '100%',
		'padding': '0.5cm'
	}}>
		<header 
			style="
				font-size: 2em; 
				text-align: center;
				padding: 0.5cm 0;
			"
		>Links</header>
		
		<p>
			<a 
				target="_blank"
				href="https://aptosfoundation.org/"
			>
				https://aptosfoundation.org/
			</a>
		</p>
		
		<p>
			<a 
				target="_blank"
				href="https://aptos.dev"
			>
				https://aptos.dev
			</a>
		</p>
		
		
		<p>
			<a 
				target="_blank"
				href="https://aptos-labs.github.io/aptos-ts-sdk/@aptos-labs/ts-sdk-1.22.2/"
			>
				https://aptos-labs.github.io/aptos-ts-sdk/@aptos-labs/ts-sdk-1.22.2/
			</a>
		</p>
		
		
		<p>
			<a 
				target="_blank"
				href="https://www.svelvet.io"
			>
				https://www.svelvet.io/
			</a>
		</p>
		
		<p>
			<a 
				target="_blank"
				href="https://flowbite-svelte.com/docs/components/buttons"
			>
				https://flowbite-svelte.com/docs/components/buttons
			</a>
		</p>
		
		<p>
			<a 
				target="_blank"
				href="https://svar.dev/svelte/core/"
			>
				https://svar.dev/svelte/core/
			</a>
		</p>
		
		<p>
			<a 
				target="_blank"
				href="https://svelteui.dev/basics"
			>
				https://svelteui.dev/basics
			</a>
		</p>
		
		<p>
			<a 
				target="_blank"
				href="https://kitschpatrol.com/svelte-tweakpane-ui"
			>
				https://kitschpatrol.com/svelte-tweakpane-ui
			</a>
		</p>
		
		<p>
			<a 
				target="_blank"
				href="https://www.npmjs.com/package/@noble/curves"
			>
				https://www.npmjs.com/package/@noble/curves
			</a>
		</p>
	</Panel>
</div>
