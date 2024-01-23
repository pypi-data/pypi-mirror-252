<script lang="ts">
  //@ts-ignore Import IS used by react:GradioWorkbook below
  import GradioWorkbook from "./GradioWorkbook";
  import { client } from "@gradio/client";

  import "./styles.css";

  import type { Gradio } from "@gradio/utils";
  import { Block } from "@gradio/atoms";
  import { StatusTracker } from "@gradio/statustracker";
  import type { LoadingStatus } from "@gradio/statustracker";
  import type { SelectData } from "@gradio/utils";
  import {
    // AIConfigEditor,
    type RunPromptStreamCallback,
    type RunPromptStreamErrorCallback,
  } from "@lastmileai/aiconfig-editor";
  import type {
    AIConfig,
    InferenceSettings,
    JSONObject,
    Prompt,
  } from "aiconfig";

  type AddPromptEventData = {
    prompt_name: string;
    prompt: Prompt;
    index: number;
  };

  type CancelRunEventData = {
    cancellation_token_id: string;
  };

  type DeletePromptEventData = {
    prompt_name: string;
  };

  type RunPromptEventData = {
    prompt_name: string;
    cancellation_token?: string;
  };

  type SetConfigDescriptionEventData = {
    description: string;
  };

  type SetConfigNameEventData = {
    name: string;
  };

  type SetParametersEventData = {
    parameters: JSONObject;
    prompt_name?: string;
  };

  type UpdateModelEventData = {
    model_name?: string;
    model_settings?: InferenceSettings;
    prompt_name?: string;
  };

  type UpdatePromptEventData = {
    prompt_name: string;
    prompt: Prompt;
  };

  export let elem_id = "";
  export let elem_classes: string[] = [];
  export let visible = true;

  // We obtain a serialized JSON string from the backend, containing
  // the aiconfig and model_ids
  export let value: string;
  let parsedValue: any;
  let aiconfig: AIConfig | undefined;
  let model_ids: string[] = [];

  // TODO: Can we just return the objects instead of serializing?
  type EventAPIResponse = {
    // Gradio client returns data as an array
    // (https://github.com/gradio-app/gradio/blob/main/client/js/src/client.ts#L40)
    // We return a JSON string on the server for the array value, so it results
    // in an array of strings
    data: string[];
  };

  // Root is provided to the component with the hostname. Rename below for clarity
  export let root: string;
  $: HOST_ENDPOINT = root;

  $: {
    try {
      if (value != null) {
        parsedValue = JSON.parse(value);
        const currentAIConfig: AIConfig | undefined =
          parsedValue.aiconfig ?? parsedValue.aiconfig_chunk;
        if (currentAIConfig) {
          aiconfig = currentAIConfig;
        }
        if (parsedValue.model_ids) {
          model_ids = parsedValue.model_ids;
        }
      }
    } catch (e) {
      console.error("Invalid JSON value passed to GradioWorkbook", e);
    }
  }

  export let container = true;
  export let scale: number | null = null;
  export let min_width: number | undefined = undefined;
  export let loading_status: LoadingStatus;
  export let gradio: Gradio<{
    change: never;
    select: SelectData;
    input: never;
    add_prompt: AddPromptEventData;
    cancel_run: CancelRunEventData;
    clear_outputs: void;
    delete_prompt: DeletePromptEventData;
    run_prompt: RunPromptEventData;
    set_config_description: SetConfigDescriptionEventData;
    set_config_name: SetConfigNameEventData;
    set_parameters: SetParametersEventData;
    update_model: UpdateModelEventData;
    update_prompt: UpdatePromptEventData;
  }>;

  async function getClient() {
    return await client(`${HOST_ENDPOINT}`, {
      /*options*/
    });
  }

  async function handleAddPrompt(
    prompt_name: string,
    prompt: Prompt,
    index: number
  ) {
    const client = await getClient();
    const res = (await client.predict("/add_prompt_impl", undefined, {
      prompt_name,
      prompt,
      index,
    })) as EventAPIResponse;

    return JSON.parse(res.data[0]);
  }

  async function handleCancel(cancellation_token_id: string) {
    const client = await getClient();
    await client.predict("/cancel_run_impl", undefined, {
      cancellation_token_id,
    });
  }

  async function handleClearOutputs() {
    const client = await getClient();
    const res = (await client.predict(
      "/clear_outputs_impl",
      undefined
    )) as EventAPIResponse;

    return JSON.parse(res.data[0]);
  }

  async function handleDeletePrompt(prompt_name: string) {
    const client = await getClient();
    await client.predict("/delete_prompt_impl", undefined, {
      prompt_name,
    });
  }

  function handleGetModels(search: string) {
    return model_ids.filter((model_id) =>
      model_id.toLowerCase().includes(search.toLowerCase())
    );
  }

  async function handleSetConfigDescription(description: string) {
    const client = await getClient();
    await client.predict("/set_config_description_impl", undefined, {
      description,
    });
  }

  async function handleSetConfigName(name: string) {
    const client = await getClient();
    await client.predict("/set_config_name_impl", undefined, {
      name,
    });
  }

  async function handleSetParameters(
    parameters: JSONObject,
    prompt_name?: string
  ) {
    const client = await getClient();
    await client.predict("/set_parameters_impl", undefined, {
      parameters,
      prompt_name,
    });
  }

  // TODO: Refactor runPrompt callback to make stream/error callbacks optional
  async function handleRunPrompt(
    prompt_name: string,
    onStream: RunPromptStreamCallback,
    onError: RunPromptStreamErrorCallback,
    _enable_streaming?: boolean,
    cancellation_token?: string
  ) {
    try {
      const client = await getClient();
      // Use submit instead of predict to handle streaming from generator endpoint
      // See https://www.gradio.app/guides/getting-started-with-the-js-client#generator-endpoints
      const stream = await client.submit("/run_prompt_impl", undefined, {
        prompt_name,
        cancellation_token,
      });

      stream.on("data", (dataEvent) => {
        const event = JSON.parse(dataEvent.data[0] as string);

        const eventType = Object.keys(event)[0] as
          | "aiconfig_chunk"
          | "output_chunk"
          | "stop_streaming"
          | "error";

        if (eventType === "error") {
          onError({
            type: "error",
            data: {
              message: event.error.message ?? "Unknown error",
              code: event.error.code ? parseInt(event.error.code) : 500,
              data: event.error.data,
            },
          });
        } else {
          onStream({
            type: eventType,
            data: event[eventType],
          });
        }
      });
    } catch (e: any) {
      onError({
        type: "error",
        data: {
          message: e.message ?? "Unknown error",
          code: 500,
          data: aiconfig!,
        },
      });
    }
  }

  function handleUpdateModel(updateRequest: {
    modelName?: string;
    settings?: InferenceSettings;
    promptName?: string;
  }) {
    gradio.dispatch("update_model", {
      prompt_name: updateRequest.promptName,
      model_name: updateRequest.modelName,
      model_settings: updateRequest.settings,
    });
  }

  async function handleUpdatePrompt(prompt_name: string, prompt: Prompt) {
    const client = await getClient();
    const res = (await client.predict("/update_prompt_impl", undefined, {
      prompt_name,
      prompt,
    })) as EventAPIResponse;

    console.log("res: ", res);

    return JSON.parse(res.data[0]);
  }
</script>

<Block {visible} {elem_id} {elem_classes} {container} {scale} {min_width}>
  {#if loading_status}
    <StatusTracker
      autoscroll={gradio.autoscroll}
      i18n={gradio.i18n}
      {...loading_status}
    />
  {/if}
  <react:GradioWorkbook
    {aiconfig}
    callbacks={{
      addPrompt: handleAddPrompt,
      cancel: handleCancel,
      clearOutputs: handleClearOutputs,
      deletePrompt: handleDeletePrompt,
      getModels: handleGetModels,
      runPrompt: handleRunPrompt,
      setConfigDescription: handleSetConfigDescription,
      setConfigName: handleSetConfigName,
      setParameters: handleSetParameters,
      updateModel: handleUpdateModel,
      updatePrompt: handleUpdatePrompt,
    }}
  />
</Block>
