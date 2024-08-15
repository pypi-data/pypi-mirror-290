

<script>
/*
	import Region_Map from '$lib/trinkets/Regions_Map/Trinket.svelte'
	<Region_Map 
		regions_map={ regions_map }
	/>
*/



/*
	regions_map = {
		"Friends": {
			"Consensus": {
				
			}
		}
	}
	
	regions_map = [{
		"name": "Friends",
		"href": "/Friends/Hints"
		"has": [{
			"name": "Consensus",
			"href": "/Friends/Hints"
		},{
			"name": "Consensus",
			"href": "/Friends/Consensus"
		},{
			"name": "Moves",
			"href": "/Friends/Moves"
		}]
	},{
		"name": "Relatives",
		"has": [{
			"name": "Addresses"
		}]
	}]


*/

export let regions_map = []

</script>

<div>
	{#each regions_map as region }


	{/each}
</div>