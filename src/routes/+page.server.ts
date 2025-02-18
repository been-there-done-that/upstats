import type { Actions, PageLoad } from './$types';
import { superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import { fail } from '@sveltejs/kit';
import { formSchema } from './monitors/[mid]/configure/schema';

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export const load: PageLoad = async ({ params }) => {
	console.log({ config: params });
	return {
		form: await superValidate(zod(formSchema))
	};
};

export const actions: Actions = {
	default: async (event) => {
		const form = await superValidate(event, zod(formSchema));
		if (!form.valid) {
			return fail(400, {
				form
			});
		}
		console.log({ form });
		return {
			form
		};
	}
};
