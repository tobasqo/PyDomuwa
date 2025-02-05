import type {PageLoad} from "./$types";
import {api} from "$lib/api";

export const load: PageLoad = async () => {
	try {
		const response = await api.get('/');
		return { props: { data: response.data } };
	} catch (err) {
		return { props: { error: (err as Error).message } };
	}
};
