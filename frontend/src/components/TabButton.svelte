<script lang="ts">
  export let text: string;
  export let selected: boolean;
  export let onclick: () => void;
</script>

<button
  class={"inline-flex items-center rounded-lg bg-lilac px-5 py-2.5 text-center text-sm font-medium text-white hover:text-mint" + (selected ? " bg-dark" : "")}
  {onclick}
>
  {text}
</button>
