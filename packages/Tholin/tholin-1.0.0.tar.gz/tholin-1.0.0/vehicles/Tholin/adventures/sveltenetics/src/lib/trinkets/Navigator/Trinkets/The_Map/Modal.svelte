

<script>


import Polytope from '$lib/trinkets/Polytope/Polytope_Modal.svelte'

import _merge from 'lodash/merge'

import { AppRail, AppRailTile, AppRailAnchor } from '@skeletonlabs/skeleton';
import { ListBox, ListBoxItem } from '@skeletonlabs/skeleton';

const prepare = () => {
	return {
		name: "Transfer",
		next: "yes",
		back: "yes"
	}
}

let polytope_modal;
const on_click = () => {
	polytope_modal.advance (({ freight }) => {
		freight.name = "panel"
		return freight;
	})
}

const on_modal_change = () => {}

let current = 1;
const on_next_pressed = () => {
	console.info ("on_next_pressed")
	
	polytope_modal.advance (({ freight }) => {
		console.log 
		
		if (freight.next.permitted === "yes") {
			current += 1
		}
		else {
			if (freight.next.has_alert === "yes") {
				freight.unfinished.showing = "yes"
			}
		}
		
		console.info ({ freight })
		
		return freight;		
	})
}

let currentTile = 0;

import Region_Map from '$lib/trinkets/Regions_Map/Trinket.svelte'
	
const regions_map = [{
	"name": "Friends",
	"href": "/Friends/Hints",
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

</script>

<style>

button {
	margin: 0.1cm 0;
}

.column-stories {
	display: flex;
	width: 100%;
}

.constant-column {
	width: 200px;
}

.hydralic-column {
	flex: 1;
}


</style>


<div 
	style="
		position: relative;
		top: 0;
		left: 0;
		padding: 0;
		width: calc(100vw - 36px);
		height: calc(100vh - 36px);
	
		overflow-y: scroll;
	"
>
	<div
		class="bg-surface-50-900-token border border-primary-500/30"
		style="
			display: flex;
			
			position: absolute;
			top: 0;
			left: 0;
			height: 100%;
			width: 100%;
			border-radius: 8px;
			
			overflow: hidden;
			
			flex-direction: column;
		"
	>
		<div
			style="
				display: flex;
				justify-content: center;
				flex-direction: column;
			"
		>
			<header
				style="
					padding: 0.2cm 0;
					text-align: center;
					font-size: 1.2em;
				"
			></header>
			<hr class="!border-t-2" />
		</div>
		
		
		
		
		<div
			class="column-stories"
			style="
				position: absolute;
				top: 50%;
				left: 50%;
				transform: translateX(-50%) translateY(-50%);
			
				display: flex;
				flex-direction: column;
				
				max-height: 100%;
				max-width: 500px;
				
				width: calc(90%);
				
				overflow-y: scroll;
			"
		>
			<Region_Map 
				regions_map={ regions_map }
			/>
		
			<div
				class="hydralic-column"
				style="
					display: flex;
					flex-direction: row;
				
					width: 100%;
					padding: 0.2cm 0;
				"
			>
				<div
					class="hydralic-column"
					style="
						display: inline-block;
						width: calc(100% - 1.1cm)
					"
				>
					<button type="button" class="btn variant-filled"
						style="
							width: 100%;
							margin: 0;
						"
					>
						<span>Athletes</span>
					</button>
				</div>
				
				<div style="width: 0.1cm"></div>
				
				<div
					class="constant-column"
					style="
						display: inline-block;
						width: 1.1cm;
					"
				>
					<button type="button" class="btn variant-filled"
						style="
							width: 1.1cm;
							height: 1.1cm;
							
							margin: 0;
						"
					>
						<span>></span>
					</button>
				</div>
			</div>
			
			<div
				class="hydralic-column"
				style="
					display: flex;
					flex-direction: row;
				
					width: 100%;
					padding: 0.2cm 0;
				"
			>
				<div
					class="hydralic-column"
					style="
						display: inline-block;
						width: calc(100% - 1.1cm)
					"
				>
					<button type="button" class="btn variant-filled"
						style="
							width: 100%;
							margin: 0;
						"
					>
						<span>Versies</span>
					</button>
				</div>
				
				<div style="width: 0.1cm"></div>
				
				<div
					class="constant-column"
					style="
						display: inline-block;
						width: 1.1cm;
					"
				>
					<button type="button" class="btn variant-filled"
						style="
							width: 1.1cm;
							height: 1.1cm;
							
							margin: 0;
						"
					>
						<span>></span>
					</button>
				</div>
			</div>
			
			<div
				class="hydralic-column"
				style="
					display: flex;
					flex-direction: row;
				
					width: 100%;
					padding: 0.2cm 0;
				"
			>
				<div
					class="hydralic-column"
					style="
						display: inline-block;
						width: calc(100% - 1.1cm)
					"
				>
					<button type="button" class="btn variant-filled"
						style="
							width: 100%;
							margin: 0;
						"
					>
						<span>Friends</span>
					</button>
				</div>
				
				<div style="width: 0.1cm"></div>
				
				<div
					class="constant-column"
					style="
						display: inline-block;
						width: 1.1cm;
					"
				>
					<button type="button" class="btn variant-filled"
						style="
							width: 1.1cm;
							height: 1.1cm;
							
							margin: 0;
						"
					>
						<span>></span>
					</button>
				</div>
			</div>
			
			<div
				class="hydralic-column"
				style="
					display: flex;
					flex-direction: row;
				
					width: 100%;
					padding: 0.2cm 0;
				"
			>
				<div
					class="hydralic-column"
					style="
						display: inline-block;
						width: calc(100% - 1.1cm)
					"
				>
					<button type="button" class="btn variant-filled"
						style="
							width: 100%;
							margin: 0;
						"
					>
						<span>Relatives</span>
					</button>
				</div>
				
				<div style="width: 0.1cm"></div>
				
				<div
					class="constant-column"
					style="
						display: inline-block;
						width: 1.1cm;
					"
				>
					<button type="button" class="btn variant-filled"
						style="
							width: 1.1cm;
							height: 1.1cm;
							
							margin: 0;
						"
					>
						<span>></span>
					</button>
				</div>
			</div>
			
			<button type="button" class="btn variant-filled">
				<span>Friends</span>
			</button>
			<button type="button" class="btn variant-filled">
				<span>Relatives</span>
			</button>
		</div>
	</div>
	
	

	
</div>
