


<script>

////
//
import { make_trends } from './screenplays/trends'
import { hexadecimalize_keys } from './screenplays/hexadecimalize_keys'
//
//
import Code_Wall from '$lib/trinkets/Code_Wall/Trinket.svelte' 
import Problem_Alert from '$lib/trinkets/Alerts/Problem.svelte'
import Info_Alert from '$lib/trinkets/Alerts/Info.svelte'
import Alert_Success from '$lib/trinkets/Alerts/Success.svelte'
import Panel from '$lib/trinkets/panel/trinket.svelte'
//
import { Account_from_private_key } from '$lib/PTO/Accounts/from_private_key'
import { parse_styles } from '$lib/trinkets/styles/parse.js';
import { save_keys } from '$lib/taverns/keys_directory/save'
//
//
import { TabGroup, Tab, TabAnchor } from '@skeletonlabs/skeleton';
import { Aptos, AptosConfig, Network } from "@aptos-labs/ts-sdk";
import { onMount } from 'svelte'
//
//
//\\


////
///
//
let seed_input_as_is;
let private_key_glyphs = ""

//
//	Aptos Wallet
//		@ Trinket
//		@ Pouch
//		@ Wallet
//		@ Account
//
let directory_name = "Aptos Wallet 1"
$: {
	let _directory_name = directory_name;
	if (directory_name.length === 0) {
		account_name_alert_problem = "The directory name needs to be at least 1 letter."
	}
	else {
		account_name_alert_problem = ""
	}
}

let alert_problem = ''
let alert_info = ''
let alert_success = ''

let account_name_alert_problem = ''

let legacy_address_hexadecimal_string = ""
let fresh_address_hexadecimal_string = ""
let private_key_hexadecimal_string = ""
let public_key_hexadecimal_string = ""
//
//\
//\\




const choose_button_trends = {
	border: "4px solid black",
	"border-radius": "4px",
	"margin": "10px 0",
	"padding": "5px",
	
	"min-width": "150px",
	
	// "box-shadow": '0 0 0 2px white, 0 0 0 4px black',
	
	"text-decoration": "solid line-through",
	"cursor": "initial",
	
	"grid-column": 2
}

let trends = make_trends ()

function save () {		
	if (public_key_hexadecimal_string.length >= 1) {
		save_keys ({
			directory_name,
			//
			legacy_address_hexadecimal_string,
			fresh_address_hexadecimal_string,
			//
			public_key_hexadecimal_string,
			//
			private_key_hexadecimal_string
		})
	}
}

const allow_save = () => {
	choose_button_trends ["text-decoration"] = "initial"
	choose_button_trends ["cursor"] = "pointer"
}
const prevent_save = () => {
	choose_button_trends ["text-decoration"] = "solid line-through"
	choose_button_trends ["cursor"] = "initial"
}

const clear_account = () => {
	legacy_address_hexadecimal_string = ""
	fresh_address_hexadecimal_string = ""
	private_key_hexadecimal_string = ""
	public_key_hexadecimal_string = ""
	
	choose_button_trends ["text-decoration"] = "solid line-through"
	choose_button_trends ["cursor"] = "initial"
}

const translation = Object.freeze ({
	"W": "0",
	"E": "1",
	"R": "2",
	"T": "3",
	
	"Y": "4",
	"U": "5",
	"I": "6",
	"O": "7",
	
	"S": "8",
	"D": "9",
	"F": "A",
	"G": "B",
	
	"H": "C",
	"J": "D",
	"K": "E",
	"L": "F"
})


const calculate_account = async () => {
	clear_account ()
	const {
		finished,
		
		alert_success: _alert_success,
		alert_info: _alert_info,
		alert_problem: _alert_problem,
		
		hexadecimal_private_key_stamps
	} = await hexadecimalize_keys ({
		keys: private_key_glyphs,
		nibble_limit: 64,
		translation
	})
	
	private_key_hexadecimal_string = hexadecimal_private_key_stamps
	
	console.log ({ private_key_hexadecimal_string, finished })
	
	alert_success = _alert_success;	
	alert_info = _alert_info;
	alert_problem = _alert_problem;

	if (finished === "yes") {
		const { 
			fresh_address_hexadecimal_string: _fresh_address_hexadecimal_string,
			legacy_address_hexadecimal_string: _legacy_address_hexadecimal_string,
			public_key_hexadecimal_string: _public_key_hexadecimal_string
		} = await Account_from_private_key ({
			private_key_hexadecimal_string: hexadecimal_private_key_stamps
		})
		
		legacy_address_hexadecimal_string = _legacy_address_hexadecimal_string
		fresh_address_hexadecimal_string = _fresh_address_hexadecimal_string
		public_key_hexadecimal_string = _public_key_hexadecimal_string
		
		allow_save ()
		
		return;
	}
}

const on_key_up = async (event) => {
	if (event.isComposing || event.keyCflavor === 229) {
		return;
	}
	
	var ctrl_key = event.ctrlKey;
	var shift_key = event.shiftKey;
	var meta_key = event.metaKey;
	var event_key = event.key;
	
	// console.log ("event_key:", { event_key })
	
	private_key_glyphs = event.target.value;
	
	await calculate_account ()
}

onMount (() => {
	calculate_account ()
})


</script>

<style>

.kbd {
	font-family: monospace;
	font-size: 1.5em;
	padding: 0.1cm 0.25cm;
}

</style>

<div address_from_keyboard_glyphs>
	<div style="height: 1.0cm"></div>

	<header
		style="
			text-align: center;
			font-size: 2em;
			line-height: 1.5em;
			max-width: 14cm;
			text-align: center;
			margin: 0 auto;
		"
	>EEC 25519 Single Key Account from Keyboard Glyph Modifier</header>

	<div style="height: 0.5cm"></div>

	<hr class="!border-t-2" />

	<div style="height: 0.5cm"></div>

	<p
		style="text-align: center;"
	>
		<span>This is for making an account that can be beautified with</span><br/>
		<span>one <b>EEC 25519 Private Key</b>.
	</p>
		

	<div style="height: 12px"></div>

	<p
		style="text-align: center;"
	>These letters:</p>

	<div style="height: 0.5cm"></div>

	<div
		style="
			display: flex;
			justify-content: center;
			flex-direction: column;
			align-items: center;			
		"
	>
		<div>
			<kbd class="kbd">W</kbd>
			<kbd class="kbd">E</kbd>
			<kbd class="kbd">R</kbd>
			<kbd class="kbd">T</kbd>
			
			<div 
				style="
					display: inline-block;
					width: 0.2cm;
				"
			></div>
			
			<kbd class="kbd">Y</kbd>
			<kbd class="kbd">U</kbd>
			<kbd class="kbd">I</kbd>
			<kbd class="kbd">O</kbd>
		</div>
		
		<div style="height: 0.5cm"></div>
		
		<div>
			<kbd class="kbd">S</kbd>
			<kbd class="kbd">D</kbd>
			<kbd class="kbd">F</kbd>
			<kbd class="kbd">G</kbd>
			
			<div 
				style="
					display: inline-block;
					width: 0.2cm;
				"
			></div>
			
			<kbd class="kbd">H</kbd>
			<kbd class="kbd">J</kbd>
			<kbd class="kbd">K</kbd>
			<kbd class="kbd">L</kbd>
		</div>
	</div>

	<div style="height: 0.5cm"></div>

	<div style="text-align: center">
		<p>are modified into hexadecimals in this group:</p>
		<p style="font-family: monospace">
			<span>0 1 2 3 4 5 6 7</span><br/>
			<span>8 9 A B C D E F</span>
		</p>
	</div>

	<div style="height: 0.5cm"></div>

	<hr class="!border-t-2" />

	<div style="height: 0.5cm"></div>

	<div style="text-align: center">
		<p>For example,</p>
		<p>WERTSDFGHJKLYUIOWERTSDFGHJKLYUIOWERTSDFGHJKLYUIOWERTSDFGHJKLYUIO</p>
		<p>creates</p>
		<p>012389ABCDEF4567012389ABCDEF4567012389ABCDEF4567012389ABCDEF4567</p>
	</div>
	
	<div style="height: 0.5cm"></div>

	<hr class="!border-t-2" />

	<div style="height: 0.5cm"></div>

	<div class="card p-4 variant-soft" style="{ trends.action }">
		<div 
			style="
				display: flex;
				justify-content: center;
			"
		>
			<span class="badge variant-soft"
				style="
					position: relative;
					font-size: 1.2em;
				"
			>
				<span>Private Key</span>
				<span class="badge variant-filled-surface">Letters</span>
			</span>
		</div>
		<div>
			<textarea
				private_key_glyphs
				
				on:keyup={ on_key_up }
				bind:this={ seed_input_as_is }
				
				rows="2"
				
				style="
					padding: 0.2cm;
				"
				class="textarea"
			/>
		</div>
	</div>
	

	
	
	{#if alert_info.length >= 1}
	<Info_Alert text={ alert_info } />
	{/if}
	
	{#if alert_problem.length >= 1}
	<Problem_Alert 
		text={ alert_problem }
	/>
	{/if}
	
	{#if alert_success.length >= 1}
	<Alert_Success 
		text={ alert_success }
	/>
	{/if}
	
	<div class="card p-4 variant-soft" style="{ trends.action }">
		<div 
			style="
				display: flex;
				justify-content: center;
			"
		>
			<span class="badge variant-soft"
				style="
					position: relative;
					font-size: 1.2em;
				"
			>
				<span>Private Key</span>
				<span class="badge variant-filled-surface">hexadecimal</span>
			</span>
		</div>
		<div private_key>
			<Code_Wall 
				text={ private_key_hexadecimal_string   } 
				context={ "" }
				can_clone={ "no" }
			/>
		</div>
	</div>
	
	<div class="card p-4 variant-soft" style="{ trends.action }">
		<div 
			style="
				display: flex;
				justify-content: center;
			"
		>
			<span class="badge variant-soft"
				style="
					position: relative;
					font-size: 1.2em;
				"
			>
				<span>Public Key</span>
				<span class="badge variant-filled-surface">hexadecimal</span>
			</span>
		</div>
		<div public_key>
			<Code_Wall 
				text={ public_key_hexadecimal_string   } 
				context={ "" }
				can_clone={ "no" }
			/>
		</div>
	</div>
	
	<div class="card p-4 variant-soft" style="{ trends.action }">
		<div 
			style="
				display: flex;
				justify-content: center;
			"
		>
			<span class="badge variant-soft"
				style="
					position: relative;
					font-size: 1.2em;
				"
			>
				<span>Legacy Address</span>
				<span class="badge variant-filled-surface">hexadecimal</span>
			</span>
		</div>
		<div legacy_address>
			<Code_Wall 
				text={ legacy_address_hexadecimal_string   } 
				context={ "" }
				can_clone={ "no" }
			/>
		</div>
	</div>
	
	<div class="card p-4 variant-soft" style="{ trends.action }">
		<div 
			style="
				display: flex;
				justify-content: center;
			"
		>
			<span class="badge variant-soft"
				style="
					position: relative;
					font-size: 1.2em;
				"
			>
				<span>Address</span>
				<span class="badge variant-filled-surface">hexadecimal</span>
			</span>
		</div>
		
		<div address>
			<Code_Wall 
				text={ fresh_address_hexadecimal_string   } 
				context={ "" }
				can_clone={ "no" }
			/>
		</div>
	</div>
	
	<div style="height: 0.5cm"></div>

	<hr class="!border-t-2" />

	<div style="height: 0.5cm"></div>

	<div class="card p-4 variant-soft" style="{ trends.action }">
		<div 
			style="
				display: flex;
				justify-content: center;
			"
		>
			<span class="badge variant-soft"
				style="
					position: relative;
					font-size: 1.2em;
				"
			>
				<span>Directory Name</span>
			</span>
		</div>
		<div>
			<textarea
				directory_name
				bind:value={ directory_name }
				
				rows="1"
				
				style="
					padding: 0.2cm 0.4cm;
				"
				class="textarea"
			/>
		</div>
	</div>
	{#if account_name_alert_problem.length >= 1}
	<Problem_Alert 
		text={ account_name_alert_problem }
	/>
	{/if}

	<div style="height: 0.1cm"></div>

	<div
		style="
			display: grid;
			grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
			gap: 4px;
			width: 100%;
			margin: 4px 0;
		"
	>

		<button 
			on:click={ save }
			style="{ parse_styles (choose_button_trends) }"
		>
			Save as Directory to OS
		</button>
	</div>
</div>