



// bun run vitest "src/lib/PTO/Accounts/Trinkets/Address_from_Keyboard/screenplays/hexadecimalize.vitest.js"



import { hexadecimalize_keys } from './hexadecimalize_keys'
//
import { describe, it, expect } from 'vitest';
import assert from 'assert'

const translation = {
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
}

describe ('hexadecimalize', () => {
	describe ('problems', async () => {
		it ('Invalid Character', async () => {
			const {
				finished,
				alert_problem,
				hexadecimal_private_key_stamps
			} = await hexadecimalize_keys ({
				keys: "1",
				nibble_limit: 64,
				translation
			})
			
			assert.equal (
				hexadecimal_private_key_stamps,
				""
			)
			assert.equal (
				finished,
				"no"
			)
			assert.equal (
				alert_problem,
				"Character 1 at 1 is not valid."
			)
		});
		
		it ('Invalid Character', async () => {
			const {
				finished,
				alert_problem,
				hexadecimal_private_key_stamps
			} = await hexadecimalize_keys ({
				keys: "SGOWYTKDHGUFIDOSYGLEYTIFJDSLGYOWOTLDHSDFGORUDKOSYWHGJJHOFIEEYFKTF",
				nibble_limit: 64,
				translation
			})
			
			assert.equal (
				hexadecimal_private_key_stamps,
				"8B7043E9CB5A69784BF1436AD98FB47073F9C89AB7259E7840CBDDC7A6114AE3"
			)
			assert.equal (
				finished,
				"no"
			)
			assert.equal (
				alert_problem,
				"There are 1 more nibbles than the limit size of 64."
			)
		});
	})
	
	describe ("not finished", () => {
		it ('not finished 1', async () => {
			const {
				finished,
				alert_problem,
				hexadecimal_private_key_stamps
			} = await hexadecimalize_keys ({
				keys: "SGO",
				nibble_limit: 64,
				translation
			})
			
			assert.equal (
				hexadecimal_private_key_stamps,
				"8B7"
			)
			assert.equal (
				finished,
				"no"
			)
			assert.equal (
				alert_problem,
				""
			)
		});
	});
	
	describe ("successful", () => {
		it ('is consistent', async () => {
			const {
				finished,
				alert_problem,
				hexadecimal_private_key_stamps
			} = await hexadecimalize_keys ({
				keys: "SGOWYTKDHGUFIDOSYGLEYTIFJDSLGYOWOTLDHSDFGORUDKOSYWHGJJHOFIEEYFKT",
				nibble_limit: 64,
				translation
			})
			
			assert.equal (
				hexadecimal_private_key_stamps,
				"8B7043E9CB5A69784BF1436AD98FB47073F9C89AB7259E7840CBDDC7A6114AE3"
			)
			assert.equal (
				finished,
				"yes"
			)
			assert.equal (
				alert_problem,
				""
			)
		});
	
	});
});
