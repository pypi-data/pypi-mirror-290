








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
import Alert_Info from '$lib/trinkets/Alerts/Info.svelte'


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
		mounted === "yes"
	) {
		make_barcode ({
			barcode_element,
			hexadecimal_string,
			size: 400
		})
	}
}

let use_zxing = "yes"
let use_bwip = "no"

let prepared = "no"
let mounted = "no"

onMount (() => {
	mounted = "yes"
	
	setTimeout (() => {
		make ()
		prepared = "yes"
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
		{#if prepared !== "yes"}
		<Alert_Info 
			text={ "preparing barcode" }
			progress={{
				show: "yes"
			}}
		/>
		{/if}
	
		{#if use_bwip === "no"}
		<div 
			bind:this={ barcode_element }
			style=""
		></div>
		{/if}
		
		{#if use_zxing === "yes"}
		<pre
			style="
				display: flex;
				justify-content: center;
			"
		>
			<code 
				id="result" 
				bind:this={ barcode_element }
			></code>
		</pre>
		{/if}
	</div>
</div>