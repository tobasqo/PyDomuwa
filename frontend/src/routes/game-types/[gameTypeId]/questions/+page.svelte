<script lang="ts">
  import QuestionsList from "$components/QuestionsList.svelte";
  import type { PageProps } from "./$types";

  const { data }: PageProps = $props();
  const { gameType, questions, excludedQuestions } = data;
</script>

<main class="mx-auto justify-center">
  <div class="max-w-screen-xl px-4 py-4 lg:px-6">
    <div class="rounded-lg bg-orange pb-1 shadow-xl">
      <div class="flex justify-between p-3">
        <h2
          class="mt-1 flex justify-between text-2xl font-bold tracking-tight text-gray-900"
        >
          {gameType.name}
        </h2>
        <div class="flex justify-end">
          <a
            class="inline-flex items-center rounded-lg bg-lilac px-5 py-2.5 text-center text-sm font-medium text-white hover:text-mint"
            href="/game-types/{gameType.id}/questions/create"
          >
            <svg
              class="-ms-1 me-1 h-5 w-5"
              fill="currentColor"
              viewBox="0 0 20 20"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                clip-rule="evenodd"
                d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
                fill-rule="evenodd"
              ></path>
            </svg>
            Stwórz pytanie
          </a>
        </div>
      </div>

      <QuestionsList {questions} {excludedQuestions} />
    </div>
  </div>
</main>
