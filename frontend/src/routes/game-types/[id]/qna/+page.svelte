<script lang="ts">
	import QuestionsList from "$components/QuestionsList.svelte";
	import type { PageProps } from "./$types";

	const { data, form }: PageProps = $props();
	const { gameType, qnaCategories, questions } = data;
	$inspect(data);
</script>

<main class="mx-auto justify-center">
	<div class="mx-auto max-w-screen-xl px-4 py-8 lg:px-6 lg:py-16">
		<div class="mb-8 rounded-lg bg-orange p-4 text-center shadow-xl">
			<h2 class="text-center text-2xl font-bold tracking-tight text-gray-900">
				{gameType.name}
			</h2>
		</div>

		<!-- TODO: add animation for in and out -->
		<!-- Main modal -->
		<div
			class="left-0 right-0 h-[calc(100%-1rem)] max-h-full w-full items-center justify-center overflow-y-auto overflow-x-hidden shadow-xl md:inset-0"
		>
			<div class="max-h-full w-full max-w-full">
				<!-- Modal content -->
				<div class="rounded-lg bg-orange">
					<!-- Modal header -->
					<div
						class="flex items-center justify-between rounded-t border-b-2 border-pink p-4"
					>
						<h3 class="text-lg font-semibold text-gray-900">Stwórz pytanie</h3>
						<!-- TODO: add onclick to close accordeon -->
						<button
							type="button"
							class="ms-auto inline-flex h-8 w-8 items-center justify-center rounded-lg bg-transparent text-sm text-gray-700 hover:bg-gray-200 hover:text-gray-900"
						>
							<svg
								class="h-3 w-3"
								aria-hidden="true"
								xmlns="http://www.w3.org/2000/svg"
								fill="none"
								viewBox="0 0 14 14"
							>
								<path
									stroke="currentColor"
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"
								/>
							</svg>
						</button>
					</div>
					<!-- Modal body -->
					<form method="POST" class="p-4 md:p-5">
						<div class="mb-4 grid grid-cols-2 gap-4">
							<div class="col-span-2">
								<label for="text" class="mb-2 block text-sm font-medium text-gray-900">
									Treść
								</label>
								<textarea
									id="text"
									name="text"
									rows="4"
									class="block w-full rounded-lg border border-rose-300 bg-slate-100 p-2.5 text-sm text-gray-900"
									placeholder="Kto z Gucci jest w stanie najwięcej wypić?"
									value={form?.text ?? ""}
									required
								></textarea>
							</div>
						</div>
						<div class="col-span-2 sm:col-span-1">
							<label for="category" class="mb-2 block text-sm font-medium text-gray-900"
								>Kategoria</label
							>
							<select
								id="game-category"
								name="game-category"
								class="block w-full rounded-lg border border-rose-300 bg-slate-100 p-2.5 text-sm text-gray-500"
								value={form?.gameCategoryId ?? ""}
								required
							>
								{#each qnaCategories as qnaCategory (qnaCategory.id)}
									<option value={qnaCategory.id}>{qnaCategory.name}</option>
								{/each}
							</select>
						</div>
						<input type="hidden" id="game-type" name="game-type" value={gameType.id} />
						{#if form?.errors }
							<div class="mt-4 space-y-2">
								{#each Object.entries(form.errors) as [field, fieldError]}
									<div class="rounded-lg bg-rose-500 p-2 text-white shadow-lg">
										<h4 class="font-bold">{field}</h4>
										<p class="text-sm">{fieldError}</p>
									</div>
								{/each}
							</div>
						{/if}
						<div class="mx-auto mt-4 flex max-w-full justify-center">
							<button
								type="submit"
								class="inline-flex items-center rounded-lg bg-lilac px-5 py-2.5 text-center text-sm font-medium text-white hover:text-mint"
							>
								<svg
									class="-ms-1 me-1 h-5 w-5"
									fill="currentColor"
									viewBox="0 0 20 20"
									xmlns="http://www.w3.org/2000/svg"
								>
									<path
										fill-rule="evenodd"
										d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
										clip-rule="evenodd"
									></path>
								</svg>
								Dodaj pytanie
							</button>
						</div>
					</form>
				</div>
			</div>
		</div>

		<QuestionsList {questions} />
	</div>
</main>
