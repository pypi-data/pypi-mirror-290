

<script>


import Polytope from '$lib/trinkets/Polytope/Polytope_Modal.svelte'

import { Autocomplete } from '@skeletonlabs/skeleton';
import { popup } from '@skeletonlabs/skeleton';
import _merge from 'lodash/merge'

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

const on_modal_change = () => {
	
}

let current = 1;
const on_next_pressed = () => {
	console.info ("on_next_pressed")
	
	polytope_modal.advance (({ freight }) => {
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

				

const on_prepare = () => {
	polytope_modal.advance (({ freight }) => {
		return _merge ({}, freight, {
			showing: 'yes',
			name: 'Transaction',
			unfinished: {
				showing: 'no',
			},
			back: {
				text: 'Back',
				permitted: "no",
				go: () => {
					console.log ('back pressed')
				}
			},
			next: {
				text: 'Unfinished',
				permitted: "no",
				has_alert: "yes",
				go: () => {
					on_next_pressed ()
				}
			},
			panel: {
				text: ''
			}
		})
		
		// freight.name = "panel"
		// freight.show = "yes"
		return freight;
	})
}

let isOpen = false;

</script>


<Polytope 
	bind:this={ polytope_modal }
	on_change={ on_modal_change }
	on_prepare={ on_prepare }
>
	<div slot="leaves"
		style="
				height: 100%;
				width: 100%;
				
				display: flex;
				justify-content: center;
				align-items: center;
			"
	>
		{#if current === 1}
		<div
			style="
				box-sizing: border-box;
				height: 100%;
				width: 100%;
				
				padding: 1cm;
				
				display: flex;
				justify-content: center;
				align-items: center;
			"
		>
			<label class="label"
				style="
					width: 100%;
				"
			>
				<header
					style="
						margin: 0 auto;
						font-size: 2em;
						text-align: center;
					"
				>Function ID</header>
				
				<div
					style="
						display: block;
						text-align: center;
						padding: 0.2cm 0;
					"
				>
					<span 
						class="badge variant-soft"
						style="
							display: inline-flex;
							position: relative;
							font-size: 1.2em;
							margin: 0 auto;
							text-align: center;
						"
					>
						<span>Example</span>
						<span class="badge variant-filled-surface">0x1::aptos_account::transfer</span>
					</span>
				</div>
				
				<textarea 
					class="textarea p-4" 
					rows="1" 
					placeholder="" 
				/>
			</label>
		</div>
		{/if}
	</div>
	
	<div slot="unfinished">
		<div>
			This is unfinished
		</div>
	</div>
</Polytope>