<script lang="ts">
  import { cubicOut } from "svelte/easing";
  import { slide } from "svelte/transition";

  export let title = "Untitled";
  let isOpen = false;
</script>

<button type="button" on:click={() => (isOpen = !isOpen)}>
  <div
    class="my-3 min-w-full cursor-pointer rounded-xl border-2 border-b-2 border-r-2 border-gray-400 bg-orange p-3 shadow-xl transition hover:bg-pink"
  >
    <div class="flex items-center justify-between">
      <h3 class="text-lg font-medium text-gray-800">{title}</h3>
      <!--	TODO: change this shit pipe	-->
      <svg
        class="h-5 w-5 transform transition-transform duration-200"
        style:transform={isOpen ? "rotate(90deg)" : "rotate(0deg)"}
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M9 517 7-7 7"
        />
      </svg>
    </div>

    {#if isOpen}
      <div
        class="mt-3 text-gray-600"
        in:slide={{ duration: 250, easing: cubicOut }}
        out:slide={{ duration: 250, easing: cubicOut }}
      >
        <slot />
      </div>
    {/if}
  </div>
</button>
