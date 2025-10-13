<script lang="ts">
	import { page } from "$app/state";

	let error = page.error;
	let details = "";
	if (error !== null) {
		details = error.message;
	}
</script>

<section>
	<div class="mx-auto max-w-screen-xl px-4 py-8 lg:px-6 lg:py-16">
		<div class="mx-auto max-w-screen-sm text-center text-slate-700">
			<h1
				class="mb-4 text-7xl font-extrabold tracking-tight text-slate-800 lg:text-9xl"
			>
				{page.status}
			</h1>
			<p class="mb-4 text-3xl font-bold tracking-tight md:text-4xl">
				Wystąpił błąd - pokaż Szantiemu
			</p>
			<p class="mb-4 text-lg font-light text-gray-700">
				{details}
			</p>
			<a
				href="/"
				class="my-4 inline-flex rounded-lg border-2 border-gray-500 bg-orange px-5 py-2.5 text-center text-sm font-medium shadow-xl hover:bg-yellow"
			>
				Powrót na stronę główną
			</a>
		</div>
	</div>
</section>
