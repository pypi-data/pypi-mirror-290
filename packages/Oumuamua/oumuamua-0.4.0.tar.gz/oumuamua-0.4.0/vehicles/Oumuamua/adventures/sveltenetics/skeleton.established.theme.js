



export const Established_Theme = {
    name: 'established',
    properties: {
		// =~= Theme Properties =~=
		"--theme-font-family-base": `ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace`,
		"--theme-font-family-heading": `ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace`,
		"--theme-font-color-base": "0 0 0",
		"--theme-font-color-dark": "255 255 255",
		"--theme-rounded-base": "9999px",
		"--theme-rounded-container": "8px",
		"--theme-border-base": "4px",
		// =~= Theme On-X Colors =~=
		"--on-primary": "0 0 0",
		"--on-secondary": "0 0 0",
		"--on-tertiary": "0 0 0",
		"--on-success": "0 0 0",
		"--on-warning": "0 0 0",
		"--on-error": "0 0 0",
		"--on-surface": "0 0 0",
		// =~= Theme Colors  =~=
		// primary | #87a7e6 
		"--color-primary-50": "237 242 251", // #edf2fb
		"--color-primary-100": "231 237 250", // #e7edfa
		"--color-primary-200": "225 233 249", // #e1e9f9
		"--color-primary-300": "207 220 245", // #cfdcf5
		"--color-primary-400": "171 193 238", // #abc1ee
		"--color-primary-500": "135 167 230", // #87a7e6
		"--color-primary-600": "122 150 207", // #7a96cf
		"--color-primary-700": "101 125 173", // #657dad
		"--color-primary-800": "81 100 138", // #51648a
		"--color-primary-900": "66 82 113", // #425271
		// secondary | #6992d7 
		"--color-secondary-50": "233 239 249", // #e9eff9
		"--color-secondary-100": "225 233 247", // #e1e9f7
		"--color-secondary-200": "218 228 245", // #dae4f5
		"--color-secondary-300": "195 211 239", // #c3d3ef
		"--color-secondary-400": "150 179 227", // #96b3e3
		"--color-secondary-500": "105 146 215", // #6992d7
		"--color-secondary-600": "95 131 194", // #5f83c2
		"--color-secondary-700": "79 110 161", // #4f6ea1
		"--color-secondary-800": "63 88 129", // #3f5881
		"--color-secondary-900": "51 72 105", // #334869
		// tertiary | #6c6dd9 
		"--color-tertiary-50": "233 233 249", // #e9e9f9
		"--color-tertiary-100": "226 226 247", // #e2e2f7
		"--color-tertiary-200": "218 219 246", // #dadbf6
		"--color-tertiary-300": "196 197 240", // #c4c5f0
		"--color-tertiary-400": "152 153 228", // #9899e4
		"--color-tertiary-500": "108 109 217", // #6c6dd9
		"--color-tertiary-600": "97 98 195", // #6162c3
		"--color-tertiary-700": "81 82 163", // #5152a3
		"--color-tertiary-800": "65 65 130", // #414182
		"--color-tertiary-900": "53 53 106", // #35356a
		// success | #33d17a 
		"--color-success-50": "224 248 235", // #e0f8eb
		"--color-success-100": "214 246 228", // #d6f6e4
		"--color-success-200": "204 244 222", // #ccf4de
		"--color-success-300": "173 237 202", // #adedca
		"--color-success-400": "112 223 162", // #70dfa2
		"--color-success-500": "51 209 122", // #33d17a
		"--color-success-600": "46 188 110", // #2ebc6e
		"--color-success-700": "38 157 92", // #269d5c
		"--color-success-800": "31 125 73", // #1f7d49
		"--color-success-900": "25 102 60", // #19663c
		// warning | #f9f06b 
		"--color-warning-50": "254 253 233", // #fefde9
		"--color-warning-100": "254 252 225", // #fefce1
		"--color-warning-200": "254 251 218", // #fefbda
		"--color-warning-300": "253 249 196", // #fdf9c4
		"--color-warning-400": "251 245 151", // #fbf597
		"--color-warning-500": "249 240 107", // #f9f06b
		"--color-warning-600": "224 216 96", // #e0d860
		"--color-warning-700": "187 180 80", // #bbb450
		"--color-warning-800": "149 144 64", // #959040
		"--color-warning-900": "122 118 52", // #7a7634
		// error | #f66151 
		"--color-error-50": "254 231 229", // #fee7e5
		"--color-error-100": "253 223 220", // #fddfdc
		"--color-error-200": "253 216 212", // #fdd8d4
		"--color-error-300": "251 192 185", // #fbc0b9
		"--color-error-400": "249 144 133", // #f99085
		"--color-error-500": "246 97 81", // #f66151
		"--color-error-600": "221 87 73", // #dd5749
		"--color-error-700": "185 73 61", // #b9493d
		"--color-error-800": "148 58 49", // #943a31
		"--color-error-900": "121 48 40", // #793028
		// surface | #955ec4 
		"--color-surface-50": "239 231 246", // #efe7f6
		"--color-surface-100": "234 223 243", // #eadff3
		"--color-surface-200": "229 215 240", // #e5d7f0
		"--color-surface-300": "213 191 231", // #d5bfe7
		"--color-surface-400": "181 142 214", // #b58ed6
		"--color-surface-500": "149 94 196", // #955ec4
		"--color-surface-600": "134 85 176", // #8655b0
		"--color-surface-700": "112 71 147", // #704793
		"--color-surface-800": "89 56 118", // #593876
		"--color-surface-900": "73 46 96", // #492e60
		
	}
}