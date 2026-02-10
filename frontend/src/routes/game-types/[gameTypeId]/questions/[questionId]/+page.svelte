<script lang="ts">
  import type {PageProps} from "./$types";

  const {data, form}: PageProps = $props();
  const {gameType, qnaCategories, question} = data;
  // TODO: assert that form is not of type never
</script>

<div
        class="mx-4 my-6 max-h-full items-center justify-center overflow-y-auto overflow-x-hidden shadow-xl md:inset-0"
>
  <div class="max-h-full w-full max-w-full">
    <div class="rounded-lg bg-orange">
      <div
              class="flex items-center justify-between rounded-t border-b-2 border-pink p-4"
      >
        <h3 class="text-base font-semibold text-gray-900">
          Edytuj pytanie dla gry <span class="italic">{gameType.name}</span>
        </h3>
      </div>
      <form method="POST" action="?/edit" class="p-4 md:p-5">
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
                    required
            >{form?.text ?? question?.text}</textarea>
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
                  required
          >
            {#each qnaCategories as qnaCategory (qnaCategory.id)}
              <option value={qnaCategory.id}
                      selected={qnaCategory.id === question?.gameCategory.id}>{qnaCategory.name}</option>
            {/each}
          </select>
        </div>
        <input type="hidden" id="game-type" name="game-type" value={gameType.id}/>
        {#if form?.errors}
          <div class="mt-4 space-y-2">
            {#each Object.entries(form?.errors) as [field, fieldError]}
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
            Zapisz pytanie
          </button>
        </div>
      </form>
      <!-- TODO: add option to delete question -->
      <!-- TODO: add question answers display -->
      <!-- TODO: add option to add answer -->
      <!-- TODO: add earlier question versions display -->
    </div>
  </div>
</div>
