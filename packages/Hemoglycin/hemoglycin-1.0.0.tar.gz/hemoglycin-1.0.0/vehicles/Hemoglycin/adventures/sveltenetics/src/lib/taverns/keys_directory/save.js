

/*
	import { save_keys } from '$lib/taverns/keys_directory/save'
	save_keys ({
		directory_name,
		//
		address_legacy_hexadecimal_string,
		address_one_sender_hexadecimal_string,
		//
		public_key_hexadecimal_string,
		//
		private_key_hexadecimal_string
	})
*/


import { dump } from 'js-yaml';
import JSZip from 'jszip'

const save_YAML_to_OS = (yamlString, fileName) => {
	console.log ({ window })
		
	const blob = new Blob([yamlString], { type: 'text/yaml' });
	const url = window.URL.createObjectURL(blob);
	const a = document.createElement('a');
	a.href = url;
	a.download = fileName || 'document.yaml';
	document.body.appendChild(a);
	a.click();    
	window.URL.revokeObjectURL(url);
	document.body.removeChild(a);
}

export const save_keys = async ({
	directory_name,
	//
	legacy_address_hexadecimal_string,
	fresh_address_hexadecimal_string,
	//
	public_key_hexadecimal_string,
	//
	private_key_hexadecimal_string
}) => {
	const name = directory_name	
	const zip = new JSZip ();
	
	console.log ("save_keys_directory", {
		directory_name,
		//
		legacy_address_hexadecimal_string,
		fresh_address_hexadecimal_string,
		//
		public_key_hexadecimal_string,
		//
		private_key_hexadecimal_string
	});
	
	const keys_dir = zip.folder (name);
	keys_dir.file (
		"Aptos.private.yaml",
		dump ({
			"Aptos Single Key": {
				"private key": {
					"format": "EEC 25519",
					"hexadecimal": private_key_hexadecimal_string
				}
			}
		},{
			quotingType: '"'
		})
	);
	
	keys_dir.file (
		"Aptos.public.yaml",
		dump ({
			"Aptos": {
				"address": {
					"hexadecimal": fresh_address_hexadecimal_string
				},
				"legacy address": {
					"hexadecimal": legacy_address_hexadecimal_string
				},
				"public key": {
					"format": "EEC 25519",
					"hexadecimal": public_key_hexadecimal_string
				}
			}
		},{
			quotingType: '"'
		})
	);
	
	zip.generateAsync ({ 
		type: "blob"
	}).
	then ((content) => {
		const link = document.createElement ('a');
		link.href = URL.createObjectURL (content);
		link.download = name + ".zip";
		link.click ();
		URL.revokeObjectURL (link.href);
	});
	
	console.log ({ zip })
	
	return;

	// Usage
	save_YAML_to_OS (dump ({
		"private key": seed_hexadecimal
	}), 'Aptos.EEC448.private-key.yaml');
	
	save_YAML_to_OS (dump ({
		"private key": seed_hexadecimal
	}), 'Aptos.EEC448.public-key.yaml');
}