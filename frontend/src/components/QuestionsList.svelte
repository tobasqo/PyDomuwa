<script lang="ts">
  import type {Question} from "$lib/api/types/question";
  import QuestionCard from "./QuestionCard.svelte";
  import TabButton from "./TabButton.svelte";

  const { questions, excludedQuestions }: { questions: Question[], excludedQuestions: Question[] } = $props();

  let selectedTab: "all" | "included" | "excluded" = $state("all");
  let selectedQuestions = $state(questions);

  function selectAllQuestions() {
    selectedTab = "all";
    selectedQuestions = [...questions, ...excludedQuestions];
  }

  function selectIncludedQuestions() {
    selectedTab = "included";
    selectedQuestions = questions;
  }

  function selectExcludedQuestions() {
    selectedTab = "excluded";
    selectedQuestions = excludedQuestions;
  }

  const tabs = [
    { text: "Wszystkie", value: "all", onclick: selectAllQuestions },
    { text: "Widoczne", value: "included", onclick: selectIncludedQuestions },
    { text: "Wykluczone", value: "excluded", onclick: selectExcludedQuestions },
  ];

</script>

<div class="flex justify-center gap-2 mb-4">
  {#each tabs as tab}
    <TabButton
      text={tab.text}
      selected={selectedTab === tab.value}
      onclick={tab.onclick}
    />
  {/each}
</div>

<ul>
  {#each selectedQuestions as question (question.id)}
    <li class="border-xl border-t-2 border-pink">
      <QuestionCard {question}/>
    </li>
  {:else}
    <p class="text-xl font-bold text-center py-4 border-t-2 border-pink">
      Nie mam pytań
    </p>
  {/each}
</ul>
