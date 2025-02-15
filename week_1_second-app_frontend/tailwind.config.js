{
	"compilerOptions": {
		"baseUrl": ".",
			"paths": {
			"@/*": ["./src/*"]
		},

		"target": "ES2022",
			"useDefineForClassFields": true,
				"lib": ["ES2023", "DOM", "DOM.Iterable"],
					"module": "ESNext",
						"skipLibCheck": true,

							/* Bundler Mode */
							"moduleResolution": "bundler",
								"allowImportingTsExtensions": true,
									"isolatedModules": true,
										"moduleDetection": "force",
											"noEmit": true,
												"jsx": "react-jsx",

													/* Linting & Code Quality */
													"strict": true,
														"noImplicitAny": true,
															"exactOptionalPropertyTypes": true,
																"forceConsistentCasingInFileNames": true,
																	"noUnusedLocals": true,
																		"noUnusedParameters": true,
																			"noFallthroughCasesInSwitch": true,
																				"allowSyntheticDefaultImports": true,
																					"resolveJsonModule": true
	},
	"include": ["src"],
		"exclude": ["node_modules", "dist"]
}
