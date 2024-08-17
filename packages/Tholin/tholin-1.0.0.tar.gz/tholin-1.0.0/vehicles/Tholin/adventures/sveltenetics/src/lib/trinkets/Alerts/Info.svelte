



<script>


/*
import Alert_Info from '$lib/trinkets/Alerts/Info.svelte'
<Alert_Info 
	text={}
	text_2={}
	progress={{
		show: "yes"
	}}
/>
*/

import Eternal_1_Progress from '$lib/trinkets/Progress/Eternal_1/Trinket.svelte'



export let text;
export let text_2 = ""
export let progress = {
	show: "no"
}


</script>

{#if typeof text === "string" && text.length >= 1}
<aside 
	class="alert variant-filled-primary" 
	style="
		position: relative;
	
		display: flex; 
		flex-direction: row;
		align-items: center;
		justify-content: center;
		
		padding: 12px; 
		margin-top: 8px
	"
>
	{#if progress.show === "yes" }
	<Eternal_1_Progress 
		width="60px"
		height="40px"
		color="#222222"
	/>
	{/if}

	<div 
		class="alert-message" 
		style="
			padding: 0 0 0 10px; 
			margin: 0;
			text-align: center;
		"
	>
		
	
		<p>{ text }</p>
		
		{#if text_2.length >= 1}
		<p>{ text_2 }</p>
		{/if}
	</div>
</aside>
{/if}