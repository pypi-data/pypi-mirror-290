

/*

*/



export const hexadecimalize_keys = ({ 
	keys,
	nibble_limit = 64,
	translation
}) => {
	let hexadecimal_private_key_stamps = ""
	
	for (let E = 0; E < keys.length; E++) {
		const stamp = keys [E].toUpperCase ();
		
		if (typeof translation [ stamp ] != "string") {
			return {
				finished: "no",
				
				alert_success: "",
				alert_info: "",
				alert_problem: `Character ${ stamp } at ${ E + 1 } is not valid.`,
				
				hexadecimal_private_key_stamps
			}
		}
		
		if (hexadecimal_private_key_stamps.length >= nibble_limit) {
			return {
				finished: "no",
				
				alert_success: "",
				alert_info: "",
				alert_problem: `There are ${ keys.length - nibble_limit } more nibbles than the limit size of ${ nibble_limit }.`,
				
				hexadecimal_private_key_stamps
			}
		}
		
		hexadecimal_private_key_stamps += translation [ stamp ];
	}
	
	if (hexadecimal_private_key_stamps.length < nibble_limit) {
		return {
			finished: "no",
			
			alert_success: "",
			alert_info: `${ hexadecimal_private_key_stamps.length } of ${ nibble_limit } characters choosen`,
			alert_problem: "",
			
			hexadecimal_private_key_stamps
		}
	}
		
	return {
		finished: "yes",
		
		alert_success: "successful",
		alert_info: '',
		alert_problem: ``,
		
		hexadecimal_private_key_stamps
	} 
}