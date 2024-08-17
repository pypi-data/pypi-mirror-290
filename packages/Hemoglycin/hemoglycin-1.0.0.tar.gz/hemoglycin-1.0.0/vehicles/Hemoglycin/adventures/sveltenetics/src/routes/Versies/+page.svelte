




<script>

import Panel from '$lib/trinkets/panel/trinket.svelte'

const text = {
	header: "Versies",
	note: "This region has the local settings that effect the dapp."
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
	<title>Versies</title>
	<meta name="description" content="Versies" />
</svelte:head>

<div 
	style="
		display: flex;
		flex: 0.6;
		justify-content: center;
		flex-direction: column;
		min-height: 100%;
	"
>
	<div 
		class="card p-4"
		style="
			padding: 1cm;
		"
	>
		<h1>{ text.header }</h1>
		<p 
			style="
				text-align: center;
				padding: .25cm 0;
			"
		>{ text.note }</p>
	</div>
</div>
