<script lang="ts">
	import "../app.css";
	import Profile from "../icons/Profile.svelte";
	import Home from "../icons/Home.svelte";

	let { children } = $props();
</script>

<nav
	class="top-0 w-full flex justify-between py-4 px-5 text-xl text-white bg-purple-600">
	<div class="">Logo</div>
	<div class="justify-between">
		<ul
			class="flex flex-wrap justify-space-between gap-5">
			<li>
				<a href="/" class="hover:underline hover:text-sky-200">
					<Home />
				</a>
			</li>
			<li>
				<a href="/profile" class="hover:underline hover:text-sky-200">
					<Profile />
				</a>
			</li>
		</ul>
	</div>
</nav>

{@render children()}
