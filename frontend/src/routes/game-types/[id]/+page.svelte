<script lang="ts">
  import QuestionsList from "$components/QuestionsList.svelte";
  import type { PageProps } from "./$types";

  const { data }: PageProps = $props();
  const { gameType, questions } = data;
</script>

<main class="mx-auto justify-center">
  <div class="max-w-screen-xl px-4 lg:px-6 py-4">
    <div class="rounded-lg bg-orange shadow-xl pb-1">
      <div class="flex justify-between p-3">
        <h2 class="flex justify-between text-2xl mt-1 font-bold tracking-tight text-gray-900">
          {gameType.name}
        </h2>
        <div class="flex justify-end">
          <a
            href="/questions?gameTypeId={gameType.id}"
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
            Stwórz pytanie
          </a>
        </div>
      </div>

      <QuestionsList {questions} />
    </div>
  </div>
</main>
