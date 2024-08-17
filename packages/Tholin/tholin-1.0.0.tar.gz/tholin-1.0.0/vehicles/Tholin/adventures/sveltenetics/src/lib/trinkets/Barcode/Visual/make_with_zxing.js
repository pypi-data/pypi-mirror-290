

/*
	make_with_zxing ({
		barcode_element, 
		packed_hexadecimal_string,
		size
	})
*/

import { BrowserQRCodeSvgWriter } from '@zxing/browser';


/*
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
*/
export const make_with_zxing = ({
	barcode_element,
	packed_hexadecimal_string,
	size
}) => {
	const code_writer = new BrowserQRCodeSvgWriter ()
	
	code_writer.writeToDom (
		barcode_element, 
		// hexadecimal_string,
		packed_hexadecimal_string,

		size, 
		size
	)
}