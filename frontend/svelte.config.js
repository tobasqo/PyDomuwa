import adapter from "@sveltejs/adapter-auto";
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";

/** @type {import("@sveltejs/kit").Config} */
const config = {
	// Consult https://svelte.dev/docs/kit/integrations
	// for more information about preprocessors
	preprocess: vitePreprocess(),
	onwarn: (warning, handler) => {
		if (warning.code.startsWith("a11y-")) return;
		handler(warning);
	},
	kit: {
		// adapter-auto only supports some environments, see https://svelte.dev/docs/kit/adapter-auto for a list.
		// If your environment is not supported, or you settled on a specific environment, switch out the adapter.
		// See https://svelte.dev/docs/kit/adapters for more information about adapters.
		adapter: adapter(),
		alias: {
			$components: "src/components",
			$lib: "src/lib",
			$stores: "src/stores",
		},
	},
	compilerOptions: {
		warningFilter: (warning) => {
			const ignore = [
				"a11y_click_events_have_key_events",
				"a11y_no_static_element_interactions",
				"a11y_consider_explicit_label",
			];
			return !ignore.includes(warning.code);
		},
	},
};

export default config;
