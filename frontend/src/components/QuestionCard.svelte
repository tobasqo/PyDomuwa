<script lang="ts">
  import type {Question} from "$lib/api/types/question";
  import GameCategoryLabel from "$components/GameCategoryLabel.svelte";

  export let question: Question;
</script>

<div class="px-3 py-2">
  <div class="flex flex-wrap justify-start">
    <h3 class="mr-2 text-lg text-gray-900">
      <span class="font-bold">Q:</span>
      <span class={"italic" + (question.excluded ? " line-through text-slate-600" : "")}>{question.text}</span>
    </h3>

    <GameCategoryLabel gameCategory={question.gameCategory} />
  </div>

  <div class="flex content-end justify-between">
    <div class="inline-block text-base">
      <span class="font-bold">Autor:</span>
      <span class="italic">{question.author.user.username}</span>
    </div>

    <div class="flex text-gray-600">
      <form method="POST"
            action="/game-types/{question.gameType.id}/questions/{question.id}?/toggleExclude">
        <button type="submit" class="hover:text-mint">
          {#if question.excluded}
            <input name="exclude" type="hidden" value="false" class="hidden"/>
            <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                    class="size-6"
            >
              <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88"
              />
            </svg>
          {:else}
            <input name="exclude" type="hidden" value="true" class="hidden"/>
            <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                    class="size-6"
            >
              <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z"
              />
              <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
              />
            </svg>
          {/if}
        </button>
      </form>

      <a href="/game-types/{question.gameType.id}/questions/{question.id}"
         class="hover:text-mint">
        <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                class="ml-2 size-5"
        >
          <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L6.832 19.82a4.5 4.5 0 0 1-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 0 1 1.13-1.897L16.863 4.487Zm0 0L19.5 7.125"
          />
        </svg>
      </a>
    </div>
  </div>
</div>
