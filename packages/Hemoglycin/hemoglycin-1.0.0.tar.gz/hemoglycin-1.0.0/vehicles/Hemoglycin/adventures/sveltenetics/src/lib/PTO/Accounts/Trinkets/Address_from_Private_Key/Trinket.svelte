


<script>

//
//
import Panel from '$lib/trinkets/panel/trinket.svelte'
import Problem_Alert from '$lib/trinkets/Alerts/Problem.svelte'
//
import { parse_styles } from '$lib/trinkets/styles/parse.js';
import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'
import { Account_from_private_key } from '$lib/PTO/Accounts/from_private_key'
import { save_keys } from '$lib/taverns/keys_directory/save'
//
//
import { clipboard } from '@skeletonlabs/skeleton';
//


let private_key_hexadecimal_string_input = ""
let private_key_hexadecimal_string = ""
let public_key_hexadecimal_string = ""

//
//	addresses
//
//
let single_key_legacy_address_hexadecimal_string = ""
let single_key_fresh_address_hexadecimal_string = ""


let alert_problem = ""
let account_name_alert_problem = ""

let directory_name = "Aptos Wallet 1"

const calculate_address = async () => {
	try {
		const single_key_account = await Account_from_private_key ({
			private_key_hexadecimal_string: private_key_hexadecimal_string_input
		})
		
		private_key_hexadecimal_string = private_key_hexadecimal_string_input
		
		single_key_legacy_address_hexadecimal_string = single_key_account.legacy_address_hexadecimal_string
		single_key_fresh_address_hexadecimal_string = single_key_account.fresh_address_hexadecimal_string
		public_key_hexadecimal_string = single_key_account.public_key_hexadecimal_string;
		
		alert_problem = ""
	}
	catch (exception) {
		alert_problem = exception.message
		
		single_key_legacy_address_hexadecimal_string = ""
		single_key_fresh_address_hexadecimal_string = ""
		
		public_key_hexadecimal_string = ""
	}
}

const save = async () => {
	save_keys ({
		directory_name,
		//
		hexadecimal_address_legacy: single_key_legacy_address_hexadecimal_string,
		hexadecimal_address_one_sender: single_key_fresh_address_hexadecimal_string,		
		//
		hexadecimal_public_key: public_key_hexadecimal_string,
		//
		hexadecimal_private_key: private_key_hexadecimal_string
	})
}

</script>

<style>

td {}

</style>

<div 
	address_from_private_key
	style="
		width: 100%;
		padding: 0.5cm;
	"
>
	<header
		style="{parse_styles ({
			'display': 'block',
			'text-align': 'center',
			'font-size': '2em',
			'padding': '1cm 0 .4cm',
			'width': '100%'
		})}"
	>Address from Private Key</header>
	<p
		style="{parse_styles ({
			'display': 'block',
			'text-align': 'center',
			'font-size': '1em',
			'word-break': 'break-word',
			'width': '100%'
		})}"
	>Example: 889ABCFED89736504127603417265389FAEDBC8F9EDABCFEB014276354526135</p>

	<div 
		style="width: 100%; background: none; margin-top: 10px"
	>
		<div 
			class="input-group-shim"
			style="
				width: 100%;
				padding: 0.1cm;
			"
		>EEC 25519 Private Key</div>
		<textarea 
			private_key_hexadecimal
			
			bind:value={ private_key_hexadecimal_string_input }
			class="textarea" 
			rows="4" 
			placeholder="" 
			style="background: none; padding: .3cm; position: relative; width: 100%"
		/>
	</div>
	
	<div
		style="{parse_styles ({
			'display': 'block',
			'text-align': 'right',
			'font-size': '2em',
			'width': '100%'
		})}"
	>
		<button 
			calculate_account
			
			type="button" 
			on:click={ calculate_address }
			
			style="margin-top: 10px"
			class="btn bg-gradient-to-br variant-gradient-primary-secondary"
		>Calculate</button>
	</div>
	
	{#if alert_problem.length >= 1}
	<div style="height: 0.1cm"></div>		
	<Problem_Alert text={ alert_problem } />
	<div style="height: 0.1cm"></div>
	{/if}
	
	<div style="height: 1cm"></div>
	
	<div class="card">
		<div class="table-container">
			<table class="table table-hover"
				style="background: none"
			>
				<tbody>
					<tr>
						<td 
							style="
								width: 30%;
								vertical-align: middle;
							"
						>Address</td>
						<td 
							style="
								width: 50%;
								vertical-align: middle;
							"
							address_hexadecimal_string
						>
							<p address_hexadecimal_string>{ single_key_fresh_address_hexadecimal_string }</p>
						</td>
						<td style="width: 20%">
							<button 
								type="button" 
								class="btn bg-gradient-to-br variant-gradient-primary-secondary"
								use:clipboard={ single_key_fresh_address_hexadecimal_string }
							>Copy</button>
						</td>
					</tr>
					
					<tr>
						<td 
							style="
								width: 30%;
								vertical-align: middle;
							"
						>Address, Legacy</td>
						<td 
							style="
								width: 50%;
								vertical-align: middle;
							"
						>
							<p legacy_address_hexadecimal_string>{ single_key_legacy_address_hexadecimal_string }</p>
						</td>
						
						<td style="width: 20%">
							<button 
								type="button" 
								class="btn bg-gradient-to-br variant-gradient-primary-secondary"
								use:clipboard={ single_key_legacy_address_hexadecimal_string }
							>Copy</button>
						</td>
					</tr>
				
					<tr>
						<td 
							style="
								width: 30%;
								vertical-align: middle;
							"
						>EEC 25519 Private Key</td>
						<td 
							style="
								width: 50%;
								vertical-align: middle;
							"
						>
							<p private_key_hexadecimal_string>{ private_key_hexadecimal_string }</p>
						</td>
						<td style="width: 20%">
							<button 
								type="button" 
								class="btn bg-gradient-to-br variant-gradient-primary-secondary"
								use:clipboard={ private_key_hexadecimal_string }
							>Copy</button>
						</td>
					</tr>
					
					<tr>
						<td 
							style="
								width: 30%;
								vertical-align: middle;
							"
						>
							<p>EEC 25519 Public Key</p>
						</td>
						<td 
							style="
								width: 50%;
								vertical-align: middle;
							"
						>
							<p public_key_hexadecimal_string>{ public_key_hexadecimal_string }</p>
						</td>
						<td style="width: 20%">
							<button 
								type="button" 
								class="btn bg-gradient-to-br variant-gradient-primary-secondary"
								use:clipboard={public_key_hexadecimal_string}
							>Copy</button>
						</td>
					</tr>
				</tbody>
			</table>
		</div>
	</div>
		
	<div style="height: 0.5cm"></div>
	
	<div class="card p-4 variant-soft">
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
				se--from-keyboard-private-key-textarea
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
			type="button" 
			on:click={ save }
			
			class="btn variant-filled-primary"
			
			style="text-decoration: strike-through"
		>
			Save as Directory to OS
		</button>
	</div>
</div>







