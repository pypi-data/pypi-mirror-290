
/*
	import { Account_from_private_key } from '$lib/PTO/Accounts/from_private_key'
	const single_key_account = await Account_from_private_key ({
		private_key_hexadecimal_string: "89ABCDEF89AB8EFD9ACB76051243760512437568C9AFEBDC89FAEDBC07615234"
	})
	
	console.info ({ single_key_account })
*/


/*
from roll: { 
	address_hexadecimal_string: "4892D45E4F4E230273E41E7FC04D9D7B622DC067ADB744F9315D089F8FF0714A", 
	public_key_hexadecimal_string: "D8FF5147736B34CC41D6E49CFC70900E42877229C6922A833DD8E98A68AAD6BF", 
	private_key_hexadecimal_string: "F4AC3E0BE4D26C2AB83C02815EFEEF07264CCCF99307EA4C8C5F32425E50FEBC" 
}
*/


//
//
import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'
import { Account_from_roll } from '$lib/PTO/Accounts/from_roll'
//
//
import * as AptosSDK from "@aptos-labs/ts-sdk";	
//
//	
	
const build_legacy_EEC_25519_Account = async ({
	private_key_hexadecimal_string
}) => {
	const private_key = new AptosSDK.Ed25519PrivateKey (
		Uint8Array_from_string (private_key_hexadecimal_string)
	)
	
	const legacy_account = AptosSDK.Account.fromPrivateKey ({ 
		privateKey: private_key, 
		legacy: true 
	});
	
	console.info ({ legacy_account })
	
	return {
		"address": string_from_Uint8Array (legacy_account.accountAddress.data),
		"private_key": string_from_Uint8Array (legacy_account.privateKey.signingKey.data),
		"public_key": string_from_Uint8Array (legacy_account.publicKey.key.data)
	}
}	

//
// https://aptos.dev/en/build/sdks/ts-sdk/account#derive-an-account-from-private-key
// (One Sender) Single Sender Ed25519
//
const build_fresh_EEC_25519_Account = async ({
	private_key_hexadecimal_string
}) => {
	const private_key = new AptosSDK.Ed25519PrivateKey (
		Uint8Array_from_string (private_key_hexadecimal_string)
	)
	const fresh_account = AptosSDK.Account.fromPrivateKey ({ 
		privateKey: private_key, 
		legacy: false 
	});
	
	console.log ({ fresh_account })
	
	return {
		"address": string_from_Uint8Array (fresh_account.accountAddress.data),
		"private_key": string_from_Uint8Array (fresh_account.privateKey.signingKey.data),
		"public_key": string_from_Uint8Array (fresh_account.publicKey.publicKey.key.data)
	}
}	




export const Account_from_private_key = async ({
	private_key_hexadecimal_string
}) => {	
	const legacy_account = await build_legacy_EEC_25519_Account ({
		private_key_hexadecimal_string
	});
	const fresh_account = await build_fresh_EEC_25519_Account ({
		private_key_hexadecimal_string
	});
	if (legacy_account ["private_key"] !== fresh_account ["private_key"]) {
		throw new Error (`The "legacy account" "private key" is different than the "one sender account" "private key".`)
	}
	if (legacy_account ["public_key"] !== fresh_account ["public_key"]) {
		throw new Error (`The "legacy account" "public key" is different than the "one sender account" "public key".`)
	}
	
	return {
		public_key_hexadecimal_string: fresh_account ["public_key"],	

		fresh_address_hexadecimal_string: fresh_account ["address"],
		legacy_address_hexadecimal_string: legacy_account ["address"]
	}
}