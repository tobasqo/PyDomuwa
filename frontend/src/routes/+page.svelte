<script lang="ts">
	export let data: any;
	export let error: string | null;
</script>

{#if error}
	<p>Error: {error}</p>
{:else if data}
	<pre>{JSON.stringify(data, null, 2)}</pre>
{:else}
	<p>Loading...</p>
{/if}
