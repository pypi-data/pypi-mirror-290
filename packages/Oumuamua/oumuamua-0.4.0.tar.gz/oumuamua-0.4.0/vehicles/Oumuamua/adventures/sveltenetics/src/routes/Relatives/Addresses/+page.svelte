



<script>

////
//
//
import { parse_styles } from '$lib/trinkets/styles/parse.js';
import Panel from '$lib/trinkets/panel/trinket.svelte'
//
import { parse_with_commas } from '$lib/taverns/numbers/parse_with_commas'
//
import Address_from_Keyboard from '$lib/PTO/Accounts/Trinkets/Address_from_Keyboard/Trinket.svelte'
import Address_from_Private_Key from '$lib/PTO/Accounts/Trinkets/Address_from_Private_Key/Trinket.svelte'
//
//
import { TabGroup, Tab, TabAnchor } from '@skeletonlabs/skeleton';
//
//\\



let tabSet = 0;
let possible_waves = parse_with_commas (
	"115792089237316195423570985008687907853269984665640564039457584007913129639936",
	{
		"with_line_breaks": "yes"
	}
)

let leaf = "from_private_key_glyphs"
const change_leaf = () => {
	leaf = event.target.value;
}

let account_variety = "EEC_25519_single_key_account"
const modify_keys_count = () => {
	account_variety = event.target.value;
}

</script>

<style>
	span {
		display: block;
	}
</style>

<svelte:head>
	<title>Addresses</title>
</svelte:head>

<main addresses>
	<Panel>
		<header
			style="{parse_styles ({
				'display': 'block',
				'text-align': 'center',
				'font-size': '2em',
				'padding': '1cm'
			})}"
		>Addresses</header>
		<p
			style="
				text-align: center;
				padding: 0 0 1cm;
			"
		>Private Keys are essentially the origin of Addresses on the block chain.</p>
		<p>
	</Panel>

	<div style="height: 20px"></div>

	<div class="card p-4">
		<header
			style="{parse_styles ({
				'display': 'block',
				'text-align': 'center',
				'font-size': '2em',
				'padding': '1cm',
			})}"
		>Abstract</header>
		<p
			style="
				padding: .5cm;
				word-wrap: break-word;
			"
		>
			<span>Addresses on the block chain can't necessarily be claimed or owned.</span>
			<br />
			<span>It's perhaps like choosing a path that takes you to a region of existence.</span>
			<span>Someone else could possibly choose the same path.</span>
			<br />
			<span>There's a path from the <b>Private Key</b> to a <b>Public Key</b>.
			<span>Also, there's a path from the <b>Public Key</b> to an <b>Address</b> or <b>Addresses</b>.</span>
			
			<br />
			<span>Mathematically speaking though, it's very unlikely that someone else coincidentally chooses the same <b>Private Key</b>.</span>
			<br />
			
			<span>Also, finding a <b>Private Key</b> from an <b>Address</b> and or <b>Public Key</b> is probably very tough.</span>
			<span>The path back is like entirely obscure.</span>
			<br />
			<span>However, if someone does somehow coincidentally find the path that you choose, then they might feel like the address at the end of the path is theirs to do with as they please.</span>
		</p>
	</div>
	
	<div style="height: 0.4cm"></div>
	
	<div class="card p-4">
		<div class="card variant-soft-primary p-4">
			<header
				style="{parse_styles ({
					'display': 'block',
					'text-align': 'center',
					'font-size': '2em',
					'padding': '1cm',
				})}"
			>Lock Mode</header>
			<select 
				keys_count
			
				class="select"
				on:change={ modify_keys_count }
			>
				<option value="EEC_25519_single_key_account">EEC 25519 Single Key</option>
				<option value="multi_key_account">Multi Key</option>
			</select>
		</div>

		
		{#if account_variety === "EEC_25519_single_key_account" }
		<div style="height: 0.4cm"></div>
		
		<div class="card variant-soft-primary p-4">
			<header
				style="{parse_styles ({
					'display': 'block',
					'text-align': 'center',
					'font-size': '2em',
					'line-height': '1.5em',
				})}"
			>
				<span>EEC 25519 Private Keys</span>
			</header>
		
			<header
				style="{parse_styles ({
					'display': 'block',
					'text-align': 'center',
					'font-size': '1em',
					'line-height': '1em',
				})}"
			>
				<span>Edward's Elliptic Curve 25519 Private Keys</span>
			</header>
			
			<div style="height: 0.4cm"></div>
			
			<span style="word-break: break-word">There are 2^256 possible Edward's Elliptic Curve (EEC) 25519 Private Keys.</span>
			<br/>
			<span style="word-break: break-word">That's</span>
			<span
				style="
					white-space: pre-wrap;
					max-width: 300px;
					margin: 0.1cm auto;
					text-align: right;
				"
			>{ possible_waves.trim () }</span>
			<span>possibilities.</span>
			
			<br/>
			<span>> 1.157 E +77</span>
		</div>
		
		<div style="height: 0.4cm"></div>
		
		<div class="card variant-soft-primary p-4">
			<header
				style="{parse_styles ({
					'display': 'block',
					'text-align': 'center',
					'font-size': '2em',
					'padding': '1cm',
				})}"
			>Address Navigator</header>
			<select 
				single_key_address_navigator
			
				class="select"
				on:change={ change_leaf }
			>
				<option value="from_private_key_glyphs">From Keyboard Glyph Modifier</option>
				<option value="from_private_key_hexadecimal">From Private Key Hexadecimal</option>
			</select>
		</div>
		
		<div style="height: 0.4cm"></div>
		
		<div class="card p-4">
			{#if leaf === "from_private_key_glyphs" }
				<Address_from_Keyboard />
			{:else if leaf === "from_private_key_hexadecimal" }
				<Address_from_Private_Key />
			{/if}
		</div>
		{:else if account_variety === "multi_key_account" }
		<div style="padding: 0.5cm">
			<p>Choosing <b>Multi Key Accounts</b> is not yet possible on this dapp.</p> 
		</div>
		{:else}
		
		{/if}
		
		
	</div>
	
	<div style="height: 15cm"></div>
</main>