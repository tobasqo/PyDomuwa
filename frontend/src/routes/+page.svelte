<script lang="ts">
	import {onMount} from "svelte";
	import { api } from "$lib/api";

	let data: any = null;
	let error: string | null = null;

	onMount(async () => {
		try {
			const response = await api.get("/");
			data = response.data;
		} catch (err) {
			error = err instanceof Error ? err.message : 'Unknown error';
		}
	});

</script>

{#if error}
	<p>Error: {error}</p>
{:else if data}
	<pre>{JSON.stringify(data, null, 2)}</pre>
{:else}
	<p>Loading...</p>
{/if}
