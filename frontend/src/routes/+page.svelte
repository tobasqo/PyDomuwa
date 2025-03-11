<script lang="ts">
	import type { PageProps } from "./$types";

	let { data }: PageProps = $props();
</script>

{#if data}
	<pre>{JSON.stringify(data, null, 2)}</pre>
{:else}
	<p>Loading...</p>
{/if}
