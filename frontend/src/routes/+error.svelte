<script lang="ts">
	import { page } from "$app/state";

	let error = page.error;
	let details = "";
	if (error !== null) {
		details = error.message;
	}
</script>


<section>
	<div class="py-8 px-4 mx-auto max-w-screen-xl lg:py-16 lg:px-6">
		<div class="mx-auto max-w-screen-sm text-center text-slate-700">
			<h1
				class="mb-4 text-7xl tracking-tight font-extrabold lg:text-9xl text-slate-800">
				{page.status}
			</h1>
			<p
				class="mb-4 text-3xl tracking-tight font-bold md:text-4xl">
				Wystąpił błąd - pokaż Szantiemu
			</p>
			<p class="mb-4 text-lg font-light text-gray-700">
				{details}
			</p>
			<a href="/"
				 class="inline-flex bg-orange hover:bg-yellow border-2 border-gray-500 shadow-xl font-medium rounded-lg text-sm px-5 py-2.5 text-center my-4">
				Powrót na stronę główną
			</a>
		</div>
	</div>
</section>
