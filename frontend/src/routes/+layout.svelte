<script lang="ts">
	import "../app.css";

	let { children } = $props();
</script>

<nav>
	<a href="/">home</a>
	<a href="/login">login</a>
</nav>

{@render children()}
