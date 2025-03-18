import type { PageLoad } from "./$types";
import { getHome } from "$lib/api";

export const load: PageLoad = async () => {
	return { state: await getHome() };
};
