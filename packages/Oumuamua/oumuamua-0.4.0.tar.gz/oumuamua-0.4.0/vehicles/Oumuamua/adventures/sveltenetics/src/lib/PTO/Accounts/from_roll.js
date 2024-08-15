
/*
	import { Account_from_roll } from '$lib/PTO/Accounts/from_roll'
	const { 
		address_hexadecimal_string,
		public_key_hexadecimal_string,
		private_key_hexadecimal_string
	} = await Account_from_roll ()
	
	console.info ({ account })
*/


import { 
	Aptos, 
	Account, 
	AccountAddress,
	AptosConfig, 
	Network, 
	SigningSchemeInput 
} from "@aptos-labs/ts-sdk";
	
import * as AptosSDK from "@aptos-labs/ts-sdk";	


/*
	AptosSDK.Account.generate ()
*/

import { ed25519 } from '@noble/curves/ed25519';

import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'

export const Account_from_roll = async () => {
	const account = AptosSDK.Account.generate ();
	
	const address_hexadecimal_string = string_from_Uint8Array (account.accountAddress.data);

	console.info (account.publicKey.key.data)
	console.info (account.privateKey.signingKey.data)


	const public_key_hexadecimal_string = string_from_Uint8Array (account.publicKey.key.data);
	const private_key_hexadecimal_string = string_from_Uint8Array (account.privateKey.signingKey.data);

	return {
		// account,
		
		address_hexadecimal_string,
		public_key_hexadecimal_string,
		
		private_key_hexadecimal_string
		
	}
}