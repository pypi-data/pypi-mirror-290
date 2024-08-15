

<script>
	import Panel from '$lib/trinkets/panel/trinket.svelte'
		
</script>

<svelte:head>
	<title>Hints</title>
</svelte:head>



<section>
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
		>Aptos</header>
		<p
			style="font-size: 1em; text-align: center"
		>This is a feature for partying with Aptos.</p>
	</Panel>

	
	<Panel 
		styles={{
			'margin': '4px',
			'width': '100%',
			'padding': '0.5cm'
		}}
	>
		<header 
			style="
				font-size: 2em; 
				text-align: center;
				padding: 0.5cm 0;
			"
		>Consent</header>
		<p 
			style="font-size: 1em; text-align: center"
		>For a gesture with this feature to be consensual, the party that makes the gesture must take full responsibility for the gesture.</p>
	</Panel>

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
		>Friends</header>
		<p
			style="font-size: 1em; text-align: center"
		>The "Friends" region requires connectivity.</p>
	</Panel>
	
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
		>Relatives</header>
		<p
			style="font-size: 1em; text-align: center"
		>The "Relatives" region has activities that should happen on a beacon that has limited connectivity.</p>
	</Panel>
	
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
		>Versies</header>
		<p
			style="font-size: 1em; text-align: center"
		>The "Versies" region is for modifying browser settings.</p>
	</Panel>
	
	
	
	
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
	}

	h1 {
		width: 100%;
	}

	.welcome {
		display: block;
		position: relative;
		width: 100%;
		height: 0;
		padding: 0 0 calc(100% * 495 / 2048) 0;
	}

	.welcome img {
		position: absolute;
		width: 100%;
		height: 100%;
		top: 0;
		display: block;
	}
</style>
