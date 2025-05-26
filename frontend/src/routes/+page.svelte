<script lang="ts">
	import type { PageProps } from "./$types";

	let { data }: PageProps = $props();
	console.log(data);
</script>

{#if data}
	<pre>{data.data}</pre>
{:else}
	<p>Loading...</p>
{/if}
