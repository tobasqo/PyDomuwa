<script lang="ts">
  import type {PageProps} from "./$types";

  const {data, form}: PageProps = $props();
  const {gameType, qnaCategories, question} = data;
  // TODO: assert that form is not of type never
</script>

<div
        class="mx-4 my-6 items-center justify-center overflow-x-hidden shadow-xl"
>
  <div class="w-full max-w-full">
    <div class="rounded-lg bg-orange">
      <div
        class="flex items-center justify-between rounded-t border-b-2 border-pink p-4"
      >
        <h3 class="text-base font-semibold text-gray-900">
          Edytuj pytanie dla gry <span class="italic">{gameType.name}</span>
        </h3>
      </div>
      <div class="mx-3 mt-2 pb-3 grid grid-cols-2 gap-2">
        <form method="POST" action="?/edit" class="p-4 md:p-5 contents">
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
          <div class="col-span-2 pb-1">
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
          <div class="inline-flex justify-center col-start-1 row-start-3">
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
              Zapisz
            </button>
          </div>
        </form>
        <div class="row-start-3 col-start-2 inline-flex justify-center">
          <form method="POST" action="?/delete">
            <!-- TODO: add confirmation dialog before submitting delete request -->
            <button
                    type="submit"
                    class="inline-flex items-center rounded-lg bg-rose-500 px-5 py-2.5 text-center text-sm font-medium text-white hover:text-mint hover:bg-rose-600"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5 mr-1">
                <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
              </svg>
              Usuń
            </button>
          </form>
        </div>
      </div>
      <!-- TODO: add question answers display -->
      <!-- TODO: add option to add answer -->
      <!-- TODO: add earlier question versions display -->
    </div>
  </div>
</div>
