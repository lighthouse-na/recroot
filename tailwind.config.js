/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ["./templates/**/*.html"],
	theme: {
		colors: {
			primary: {
				DEFAULT: "#E56114",
				50: "#FFF7ED",
				100: "#FFEDD5",
				200: "#FED7AA",
				300: "#FDBA74",
				400: "#FB923C",
				500: "#F97316",
				600: "#EA580C",
				700: "#C2410C",
				800: "#9A3412",
				900: "#7C2D12",
				950: "#66240D",
			},
			secondary: {
				DEFAULT: "#0057B8",
				50: "#F0F5F9",
				100: "#D9E2EC",
				200: "#A0AEC0",
				300: "#6886A0",
				400: "#4F748E",
				500: "#013569",
				600: "#012D5A",
				700: "#00274E",
				800: "#002145",
				900: "#001D3E",
				950: "#001833",
			},
		},
		extend: {},
	},
	plugins: [],
};
