# Codebase description #

## Operating System ##

You have command line access.

## Tech Stack - Next.js (TypeScript) with Supabase ##

You are working with Next.js (TypeScript), with the App router enabled.
The app Router

In version 13, Next.js introduced a new App Router built on React Server Components, which supports shared layouts, nested routing, loading states, error handling, and more.

The App Router works in a new directory named app. The app directory works alongside the pages directory to allow for incremental adoption. This allows you to opt some routes of your application into the new behavior while keeping other routes in the pages directory for previous behavior. If your application uses the pages directory, please also see the Pages Router documentation.

    Good to know: The App Router takes priority over the Pages Router. Routes across directories should not resolve to the same URL path and will cause a build-time error to prevent a conflict.

Next.js App Directory

By default, components inside app are React Server Components. This is a performance optimization and allows you to easily adopt them, and you can also use Client Components.

    Recommendation: Check out the Server page if you're new to Server Components.

Roles of Folders and Files

Next.js uses a file-system based router where:

    Folders are used to define routes. A route is a single path of nested folders, following the file-system hierarchy from the root folder down to a final leaf folder that includes a page.js file. See Defining Routes.
    Files are used to create UI that is shown for a route segment. See special files.

Route Segments

Each folder in a route represents a route segment. Each route segment is mapped to a corresponding segment in a URL path.
How Route Segments Map to URL Segments
Nested Routes

To create a nested route, you can nest folders inside each other. For example, you can add a new /dashboard/settings route by nesting two new folders in the app directory.

The /dashboard/settings route is composed of three segments:

    / (Root segment)
    dashboard (Segment)
    settings (Leaf segment)

File Conventions

Next.js provides a set of special files to create UI with specific behavior in nested routes:
	
layout	Shared UI for a segment and its children
page	Unique UI of a route and make routes publicly accessible
loading	Loading UI for a segment and its children
not-found	Not found UI for a segment and its children
error	Error UI for a segment and its children
global-error	Global Error UI
route	Server-side API endpoint
template	Specialized re-rendered Layout UI
default	Fallback UI for Parallel Routes

    Good to know: .js, .jsx, or .tsx file extensions can be used for special files.

Component Hierarchy

The React components defined in special files of a route segment are rendered in a specific hierarchy:

    layout.js
    template.js
    error.js (React error boundary)
    loading.js (React suspense boundary)
    not-found.js (React error boundary)
    page.js or nested layout.js

Component Hierarchy for File Conventions

In a nested route, the components of a segment will be nested inside the components of its parent segment.
Nested File Conventions Component Hierarchy
Colocation

In addition to special files, you have the option to colocate your own files (e.g. components, styles, tests, etc) inside folders in the app directory.

This is because while folders define routes, only the contents returned by page.js or route.js are publicly addressable.
An example folder structure with colocated files

Learn more about Project Organization and Colocation.
Advanced Routing Patterns

The App Router also provides a set of conventions to help you implement more advanced routing patterns. These include:

    Parallel Routes: Allow you to simultaneously show two or more pages in the same view that can be navigated independently. You can use them for split views that have their own sub-navigation. E.g. Dashboards.
    Intercepting Routes: Allow you to intercept a route and show it in the context of another route. You can use these when keeping the context for the current page is important. E.g. Seeing all tasks while editing one task or expanding a photo in a feed.

These patterns allow you to build richer and more complex UIs, democratizing features that were historically complex for small teams and individual developers to implement.

Server Actions and Mutations

Server Actions are asynchronous functions that are executed on the server. They can be used in Server and Client Components to handle form submissions and data mutations in Next.js applications.

    🎥 Watch: Learn more about forms and mutations with Server Actions → YouTube (10 minutes)

    .

Convention

A Server Action can be defined with the React "use server"

directive. You can place the directive at the top of an async function to mark the function as a Server Action, or at the top of a separate file to mark all exports of that file as Server Actions.
Server Components

Server Components can use the inline function level or module level "use server" directive. To inline a Server Action, add "use server" to the top of the function body:
app/page.tsx

// Server Component
export default function Page() {
  // Server Action
  async function create() {
    'use server'
 
    // ...
  }
 
  return (
    // ...
  )
}

Client Components

Client Components can only import actions that use the module-level "use server" directive.

To call a Server Action in a Client Component, create a new file and add the "use server" directive at the top of it. All functions within the file will be marked as Server Actions that can be reused in both Client and Server Components:
app/actions.ts

'use server'
 
export async function create() {
  // ...
}

app/ui/button.tsx

import { create } from '@/app/actions'
 
export function Button() {
  return (
    // ...
  )
}

You can also pass a Server Action to a Client Component as a prop:

<ClientComponent updateItem={updateItem} />

app/client-component.jsx

'use client'
 
export default function ClientComponent({ updateItem }) {
  return <form action={updateItem}>{/* ... */}</form>
}

Behavior

    Server actions can be invoked using the action attribute in a <form> element:
        Server Components support progressive enhancement by default, meaning the form will be submitted even if JavaScript hasn't loaded yet or is disabled.
        In Client Components, forms invoking Server Actions will queue submissions if JavaScript isn't loaded yet, prioritizing client hydration.
        After hydration, the browser does not refresh on form submission.
    Server Actions are not limited to <form> and can be invoked from event handlers, useEffect, third-party libraries, and other form elements like <button>.
    Server Actions integrate with the Next.js caching and revalidation architecture. When an action is invoked, Next.js can return both the updated UI and new data in a single server roundtrip.
    Behind the scenes, actions use the POST method, and only this HTTP method can invoke them.
    The arguments and return value of Server Actions must be serializable by React. See the React docs for a list of serializable arguments and values

    .
    Server Actions are functions. This means they can be reused anywhere in your application.
    Server Actions inherit the runtime from the page or layout they are used on.
    Server Actions inherit the Route Segment Config from the page or layout they are used on, including fields like maxDuration.

Examples
Forms

React extends the HTML <form>

element to allow Server Actions to be invoked with the action prop.

When invoked in a form, the action automatically receives the FormData
object. You don't need to use React useState to manage fields, instead, you can extract the data using the native FormData methods

:
app/invoices/page.tsx

export default function Page() {
  async function createInvoice(formData: FormData) {
    'use server'
 
    const rawFormData = {
      customerId: formData.get('customerId'),
      amount: formData.get('amount'),
      status: formData.get('status'),
    }
 
    // mutate data
    // revalidate cache
  }
 
  return <form action={createInvoice}>...</form>
}

    Good to know:

        Example: Form with Loading & Error States

When working with forms that have many fields, you may want to consider using the entries()
method with JavaScript's Object.fromEntries()
. For example: const rawFormData = Object.fromEntries(formData.entries()). One thing to note is that the formData will include additional $ACTION_properties.
See React <form> documentation

        to learn more.

Passing Additional Arguments

You can pass additional arguments to a Server Action using the JavaScript bind method.
app/client-component.tsx

'use client'
 
import { updateUser } from './actions'
 
export function UserProfile({ userId }: { userId: string }) {
  const updateUserWithId = updateUser.bind(null, userId)
 
  return (
    <form action={updateUserWithId}>
      <input type="text" name="name" />
      <button type="submit">Update User Name</button>
    </form>
  )
}

The Server Action will receive the userId argument, in addition to the form data:
app/actions.js

'use server'
 
export async function updateUser(userId, formData) {
  // ...
}

    Good to know:

        An alternative is to pass arguments as hidden input fields in the form (e.g. <input type="hidden" name="userId" value={userId} />). However, the value will be part of the rendered HTML and will not be encoded.
        .bind works in both Server and Client Components. It also supports progressive enhancement.

Pending states

You can use the React useFormStatus

hook to show a pending state while the form is being submitted.

    useFormStatus returns the status for a specific <form>, so it must be defined as a child of the <form> element.
    useFormStatus is a React hook and therefore must be used in a Client Component.

app/submit-button.tsx

'use client'
 
import { useFormStatus } from 'react-dom'
 
export function SubmitButton() {
  const { pending } = useFormStatus()
 
  return (
    <button type="submit" aria-disabled={pending}>
      Add
    </button>
  )
}

<SubmitButton /> can then be nested in any form:
app/page.tsx

import { SubmitButton } from '@/app/submit-button'
import { createItem } from '@/app/actions'
 
// Server Component
export default async function Home() {
  return (
    <form action={createItem}>
      <input type="text" name="field-name" />
      <SubmitButton />
    </form>
  )
}

Server-side validation and error handling

We recommend using HTML validation like required and type="email" for basic client-side form validation.

For more advanced server-side validation, you can use a library like zod

to validate the form fields before mutating the data:
app/actions.ts

'use server'
 
import { z } from 'zod'
 
const schema = z.object({
  email: z.string({
    invalid_type_error: 'Invalid Email',
  }),
})
 
export default async function createUser(formData: FormData) {
  const validatedFields = schema.safeParse({
    email: formData.get('email'),
  })
 
  // Return early if the form data is invalid
  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
    }
  }
 
  // Mutate data
}

Once the fields have been validated on the server, you can return a serializable object in your action and use the React useFormState

hook to show a message to the user.

    By passing the action to useFormState, the action's function signature changes to receive a new prevState or initialState parameter as its first argument.
    useFormState is a React hook and therefore must be used in a Client Component.

app/actions.ts

'use server'
 
export async function createUser(prevState: any, formData: FormData) {
  // ...
  return {
    message: 'Please enter a valid email',
  }
}

Then, you can pass your action to the useFormState hook and use the returned state to display an error message.
app/ui/signup.tsx

'use client'
 
import { useFormState } from 'react-dom'
import { createUser } from '@/app/actions'
 
const initialState = {
  message: '',
}
 
export function Signup() {
  const [state, formAction] = useFormState(createUser, initialState)
 
  return (
    <form action={formAction}>
      <label htmlFor="email">Email</label>
      <input type="text" id="email" name="email" required />
      {/* ... */}
      <p aria-live="polite" className="sr-only">
        {state?.message}
      </p>
      <button>Sign up</button>
    </form>
  )
}

    Good to know:

        Before mutating data, you should always ensure a user is also authorized to perform the action. See Authentication and Authorization.

Optimistic updates

You can use the React useOptimistic

hook to optimistically update the UI before the Server Action finishes, rather than waiting for the response:
app/page.tsx

'use client'
 
import { useOptimistic } from 'react'
import { send } from './actions'
 
type Message = {
  message: string
}
 
export function Thread({ messages }: { messages: Message[] }) {
  const [optimisticMessages, addOptimisticMessage] = useOptimistic<Message[]>(
    messages,
    (state: Message[], newMessage: string) => [
      ...state,
      { message: newMessage },
    ]
  )
 
  return (
    <div>
      {optimisticMessages.map((m, k) => (
        <div key={k}>{m.message}</div>
      ))}
      <form
        action={async (formData: FormData) => {
          const message = formData.get('message')
          addOptimisticMessage(message)
          await send(message)
        }}
      >
        <input type="text" name="message" />
        <button type="submit">Send</button>
      </form>
    </div>
  )
}

Nested elements

You can invoke a Server Action in elements nested inside <form> such as <button>, <input type="submit">, and <input type="image">. These elements accept the formAction prop or event handlers.

This is useful in cases where you want to call multiple server actions within a form. For example, you can create a specific <button> element for saving a post draft in addition to publishing it. See the React <form> docs

for more information.
Programmatic form submission

You can trigger a form submission using the requestSubmit()

method. For example, when the user presses ⌘ + Enter, you can listen for the onKeyDown event:
app/entry.tsx

'use client'
 
export function Entry() {
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (
      (e.ctrlKey || e.metaKey) &&
      (e.key === 'Enter' || e.key === 'NumpadEnter')
    ) {
      e.preventDefault()
      e.currentTarget.form?.requestSubmit()
    }
  }
 
  return (
    <div>
      <textarea name="entry" rows={20} required onKeyDown={handleKeyDown} />
    </div>
  )
}

This will trigger the submission of the nearest <form> ancestor, which will invoke the Server Action.
Non-form Elements

While it's common to use Server Actions within <form> elements, they can also be invoked from other parts of your code such as event handlers and useEffect.
Event Handlers

You can invoke a Server Action from event handlers such as onClick. For example, to increment a like count:
app/like-button.tsx

'use client'
 
import { incrementLike } from './actions'
import { useState } from 'react'
 
export default function LikeButton({ initialLikes }: { initialLikes: number }) {
  const [likes, setLikes] = useState(initialLikes)
 
  return (
    <>
      <p>Total Likes: {likes}</p>
      <button
        onClick={async () => {
          const updatedLikes = await incrementLike()
          setLikes(updatedLikes)
        }}
      >
        Like
      </button>
    </>
  )
}

To improve the user experience, we recommend using other React APIs like useOptimistic
and useTransition

to update the UI before the Server Action finishes executing on the server, or to show a pending state.

You can also add event handlers to form elements, for example, to save a form field onChange:
app/ui/edit-post.tsx

'use client'
 
import { publishPost, saveDraft } from './actions'
 
export default function EditPost() {
  return (
    <form action={publishPost}>
      <textarea
        name="content"
        onChange={async (e) => {
          await saveDraft(e.target.value)
        }}
      />
      <button type="submit">Publish</button>
    </form>
  )
}

For cases like this, where multiple events might be fired in quick succession, we recommend debouncing to prevent unnecessary Server Action invocations.
useEffect

You can use the React useEffect

hook to invoke a Server Action when the component mounts or a dependency changes. This is useful for mutations that depend on global events or need to be triggered automatically. For example, onKeyDown for app shortcuts, an intersection observer hook for infinite scrolling, or when the component mounts to update a view count:
app/view-count.tsx

'use client'
 
import { incrementViews } from './actions'
import { useState, useEffect } from 'react'
 
export default function ViewCount({ initialViews }: { initialViews: number }) {
  const [views, setViews] = useState(initialViews)
 
  useEffect(() => {
    const updateViews = async () => {
      const updatedViews = await incrementViews()
      setViews(updatedViews)
    }
 
    updateViews()
  }, [])
 
  return <p>Total Views: {views}</p>
}

Remember to consider the behavior and caveats

of useEffect.
Error Handling

When an error is thrown, it'll be caught by the nearest error.js or <Suspense> boundary on the client. We recommend using try/catch to return errors to be handled by your UI.

For example, your Server Action might handle errors from creating a new item by returning a message:
app/actions.ts

'use server'
 
export async function createTodo(prevState: any, formData: FormData) {
  try {
    // Mutate data
  } catch (e) {
    throw new Error('Failed to create task')
  }
}

    Good to know:

        Aside from throwing the error, you can also return an object to be handled by useFormState. See Server-side validation and error handling.

Revalidating data

You can revalidate the Next.js Cache inside your Server Actions with the revalidatePath API:
app/actions.ts

'use server'
 
import { revalidatePath } from 'next/cache'
 
export async function createPost() {
  try {
    // ...
  } catch (error) {
    // ...
  }
 
  revalidatePath('/posts')
}

Or invalidate a specific data fetch with a cache tag using revalidateTag:
app/actions.ts

'use server'
 
import { revalidateTag } from 'next/cache'
 
export async function createPost() {
  try {
    // ...
  } catch (error) {
    // ...
  }
 
  revalidateTag('posts')
}

Redirecting

If you would like to redirect the user to a different route after the completion of a Server Action, you can use redirect API. redirect needs to be called outside of the try/catch block:
app/actions.ts

'use server'
 
import { redirect } from 'next/navigation'
import { revalidateTag } from 'next/cache'
 
export async function createPost(id: string) {
  try {
    // ...
  } catch (error) {
    // ...
  }
 
  revalidateTag('posts') // Update cached posts
  redirect(`/post/${id}`) // Navigate to the new post page
}

Cookies

You can get, set, and delete cookies inside a Server Action using the cookies API:
app/actions.ts

'use server'
 
import { cookies } from 'next/headers'
 
export async function exampleAction() {
  // Get cookie
  const value = cookies().get('name')?.value
 
  // Set cookie
  cookies().set('name', 'Delba')
 
  // Delete cookie
  cookies().delete('name')
}

See additional examples for deleting cookies from Server Actions.

Patterns and Best Practices

There are a few recommended patterns and best practices for fetching data in React and Next.js. This page will go over some of the most common patterns and how to use them.
Fetching data on the server

Whenever possible, we recommend fetching data on the server with Server Components. This allows you to:

    Have direct access to backend data resources (e.g. databases).
    Keep your application more secure by preventing sensitive information, such as access tokens and API keys, from being exposed to the client.
    Fetch data and render in the same environment. This reduces both the back-and-forth communication between client and server, as well as the work on the main thread

    on the client.
    Perform multiple data fetches with single round-trip instead of multiple individual requests on the client.
    Reduce client-server waterfalls.
    Depending on your region, data fetching can also happen closer to your data source, reducing latency and improving performance.

Then, you can mutate or update data with Server Actions.
Fetching data where it's needed

If you need to use the same data (e.g. current user) in multiple components in a tree, you do not have to fetch data globally, nor forward props between components. Instead, you can use fetch or React cache in the component that needs the data without worrying about the performance implications of making multiple requests for the same data.

This is possible because fetch requests are automatically memoized. Learn more about request memoization

    Good to know: This also applies to layouts, since it's not possible to pass data between a parent layout and its children.

Server Components

React Server Components allow you to write UI that can be rendered and optionally cached on the server. In Next.js, the rendering work is further split by route segments to enable streaming and partial rendering, and there are three different server rendering strategies:

    Static Rendering
    Dynamic Rendering
    Streaming

This page will go through how Server Components work, when you might use them, and the different server rendering strategies.
Benefits of Server Rendering

There are a couple of benefits to doing the rendering work on the server, including:

    Data Fetching: Server Components allow you to move data fetching to the server, closer to your data source. This can improve performance by reducing time it takes to fetch data needed for rendering, and the number of requests the client needs to make.
    Security: Server Components allow you to keep sensitive data and logic on the server, such as tokens and API keys, without the risk of exposing them to the client.
    Caching: By rendering on the server, the result can be cached and reused on subsequent requests and across users. This can improve performance and reduce cost by reducing the amount of rendering and data fetching done on each request.
    Bundle Sizes: Server Components allow you to keep large dependencies that previously would impact the client JavaScript bundle size on the server. This is beneficial for users with slower internet or less powerful devices, as the client does not have to download, parse and execute any JavaScript for Server Components.
    Initial Page Load and First Contentful Paint (FCP)

    : On the server, we can generate HTML to allow users to view the page immediately, without waiting for the client to download, parse and execute the JavaScript needed to render the page.
    Search Engine Optimization and Social Network Shareability: The rendered HTML can be used by search engine bots to index your pages and social network bots to generate social card previews for your pages.
    Streaming: Server Components allow you to split the rendering work into chunks and stream them to the client as they become ready. This allows the user to see parts of the page earlier without having to wait for the entire page to be rendered on the server.

Using Server Components in Next.js

By default, Next.js uses Server Components. This allows you to automatically implement server rendering with no additional configuration, and you can opt into using Client Components when needed, see Client Components.
How are Server Components rendered?

On the server, Next.js uses React's APIs to orchestrate rendering. The rendering work is split into chunks: by individual route segments and Suspense Boundaries

.

Each chunk is rendered in two steps:

    React renders Server Components into a special data format called the React Server Component Payload (RSC Payload).
    Next.js uses the RSC Payload and Client Component JavaScript instructions to render HTML on the server.

Then, on the client:

    The HTML is used to immediately show a fast non-interactive preview of the route - this is for the initial page load only.
    The React Server Components Payload is used to reconcile the Client and Server Component trees, and update the DOM.
    The JavaScript instructions are used to hydrate

    Client Components and make the application interactive.

    What is the React Server Component Payload (RSC)?

    The RSC Payload is a compact binary representation of the rendered React Server Components tree. It's used by React on the client to update the browser's DOM. The RSC Payload contains:

        The rendered result of Server Components
        Placeholders for where Client Components should be rendered and references to their JavaScript files
        Any props passed from a Server Component to a Client Component

Server Rendering Strategies

There are three subsets of server rendering: Static, Dynamic, and Streaming.
Static Rendering (Default)

With Static Rendering, routes are rendered at build time, or in the background after data revalidation. The result is cached and can be pushed to a Content Delivery Network (CDN)

. This optimization allows you to share the result of the rendering work between users and server requests.

Static rendering is useful when a route has data that is not personalized to the user and can be known at build time, such as a static blog post or a product page.
Dynamic Rendering

With Dynamic Rendering, routes are rendered for each user at request time.

Dynamic rendering is useful when a route has data that is personalized to the user or has information that can only be known at request time, such as cookies or the URL's search params.

    Dynamic Routes with Cached Data

    In most websites, routes are not fully static or fully dynamic - it's a spectrum. For example, you can have an e-commerce page that uses cached product data that's revalidated at an interval, but also has uncached, personalized customer data.

    In Next.js, you can have dynamically rendered routes that have both cached and uncached data. This is because the RSC Payload and data are cached separately. This allows you to opt into dynamic rendering without worrying about the performance impact of fetching all the data at request time.

    Learn more about the full-route cache and Data Cache.

Switching to Dynamic Rendering

During rendering, if a dynamic function or uncached data request is discovered, Next.js will switch to dynamically rendering the whole route. This table summarizes how dynamic functions and data caching affect whether a route is statically or dynamically rendered:
Dynamic Functions	Data	Route
No	Cached	Statically Rendered
Yes	Cached	Dynamically Rendered
No	Not Cached	Dynamically Rendered
Yes	Not Cached	Dynamically Rendered

In the table above, for a route to be fully static, all data must be cached. However, you can have a dynamically rendered route that uses both cached and uncached data fetches.

As a developer, you do not need to choose between static and dynamic rendering as Next.js will automatically choose the best rendering strategy for each route based on the features and APIs used. Instead, you choose when to cache or revalidate specific data, and you may choose to stream parts of your UI.
Dynamic Functions

Dynamic functions rely on information that can only be known at request time such as a user's cookies, current requests headers, or the URL's search params. In Next.js, these dynamic functions are:

    cookies() and headers(): Using these in a Server Component will opt the whole route into dynamic rendering at request time.
    searchParams: Using the Pages prop will opt the page into dynamic rendering at request time.

Using any of these functions will opt the whole route into dynamic rendering at request time.

Client Components

Client Components allow you to write interactive UI that is prerendered on the server

and can use client JavaScript to run in the browser.

This page will go through how Client Components work, how they're rendered, and when you might use them.
Benefits of Client Rendering

There are a couple of benefits to doing the rendering work on the client, including:

    Interactivity: Client Components can use state, effects, and event listeners, meaning they can provide immediate feedback to the user and update the UI.
    Browser APIs: Client Components have access to browser APIs, like geolocation

or localStorage

    .

Using Client Components in Next.js

To use Client Components, you can add the React "use client" directive

at the top of a file, above your imports.

"use client" is used to declare a boundary between a Server and Client Component modules. This means that by defining a "use client" in a file, all other modules imported into it, including child components, are considered part of the client bundle.
app/counter.tsx

'use client'
 
import { useState } from 'react'
 
export default function Counter() {
  const [count, setCount] = useState(0)
 
  return (
    <div>
      <p>You clicked {count} times</p>
      <button onClick={() => setCount(count + 1)}>Click me</button>
    </div>
  )
}

The diagram below shows that using onClick and useState in a nested component (toggle.js) will cause an error if the "use client" directive is not defined. This is because, by default, all components in the App Router are Server Components where these APIs are not available. By defining the "use client" directive in toggle.js, you can tell React to enter the client boundary where these APIs are available.
Use Client Directive and Network Boundary

    Defining multiple use client entry points:

    You can define multiple "use client" entry points in your React Component tree. This allows you to split your application into multiple client bundles.

    However, "use client" doesn't need to be defined in every component that needs to be rendered on the client. Once you define the boundary, all child components and modules imported into it are considered part of the client bundle.

How are Client Components Rendered?

In Next.js, Client Components are rendered differently depending on whether the request is part of a full page load (an initial visit to your application or a page reload triggered by a browser refresh) or a subsequent navigation.
Full page load

To optimize the initial page load, Next.js will use React's APIs to render a static HTML preview on the server for both Client and Server Components. This means, when the user first visits your application, they will see the content of the page immediately, without having to wait for the client to download, parse, and execute the Client Component JavaScript bundle.

On the server:

    React renders Server Components into a special data format called the React Server Component Payload (RSC Payload), which includes references to Client Components.
    Next.js uses the RSC Payload and Client Component JavaScript instructions to render HTML for the route on the server.

Then, on the client:

    The HTML is used to immediately show a fast non-interactive initial preview of the route.
    The React Server Components Payload is used to reconcile the Client and Server Component trees, and update the DOM.
    The JavaScript instructions are used to hydrate

    Client Components and make their UI interactive.

    What is hydration?

    Hydration is the process of attaching event listeners to the DOM, to make the static HTML interactive. Behind the scenes, hydration is done with the hydrateRoot

React API.

Server and Client Composition Patterns

When building React applications, you will need to consider what parts of your application should be rendered on the server or the client. This page covers some recommended composition patterns when using Server and Client Components.

Server Component Patterns

Before opting into client-side rendering, you may wish to do some work on the server like fetching data, or accessing your database or backend services.

Here are some common patterns when working with Server Components:
Sharing data between components

When fetching data on the server, there may be cases where you need to share data across different components. For example, you may have a layout and a page that depend on the same data.

Instead of using React Context

(which is not available on the server) or passing data as props, you can use fetch or React's cache function to fetch the same data in the components that need it, without worrying about making duplicate requests for the same data. This is because React extends fetch to automatically memoize data requests, and the cache function can be used when fetch is not available.

Learn more about memoization in React.
Keeping Server-only Code out of the Client Environment

Since JavaScript modules can be shared between both Server and Client Components modules, it's possible for code that was only ever intended to be run on the server to sneak its way into the client.

For example, take the following data-fetching function:
lib/data.ts

export async function getData() {
  const res = await fetch('https://external-service.com/data', {
    headers: {
      authorization: process.env.API_KEY,
    },
  })
 
  return res.json()
}

At first glance, it appears that getData works on both the server and the client. However, this function contains an API_KEY, written with the intention that it would only ever be executed on the server.

Since the environment variable API_KEY is not prefixed with NEXT_PUBLIC, it's a private variable that can only be accessed on the server. To prevent your environment variables from being leaked to the client, Next.js replaces private environment variables with an empty string.

As a result, even though getData() can be imported and executed on the client, it won't work as expected. And while making the variable public would make the function work on the client, you may not want to expose sensitive information to the client.

To prevent this sort of unintended client usage of server code, we can use the server-only package to give other developers a build-time error if they ever accidentally import one of these modules into a Client Component.

To use server-only, first install the package:
Terminal

npm install server-only

Then import the package into any module that contains server-only code:
lib/data.js

import 'server-only'
 
export async function getData() {
  const res = await fetch('https://external-service.com/data', {
    headers: {
      authorization: process.env.API_KEY,
    },
  })
 
  return res.json()
}

Now, any Client Component that imports getData() will receive a build-time error explaining that this module can only be used on the server.

The corresponding package client-only can be used to mark modules that contain client-only code – for example, code that accesses the window object.
Using Third-party Packages and Providers

Since Server Components are a new React feature, third-party packages and providers in the ecosystem are just beginning to add the "use client" directive to components that use client-only features like useState, useEffect, and createContext.

Today, many components from npm packages that use client-only features do not yet have the directive. These third-party components will work as expected within Client Components since they have the "use client" directive, but they won't work within Server Components.

For example, let's say you've installed the hypothetical acme-carousel package which has a <Carousel /> component. This component uses useState, but it doesn't yet have the "use client" directive.

If you use <Carousel /> within a Client Component, it will work as expected:
app/gallery.tsx

'use client'
 
import { useState } from 'react'
import { Carousel } from 'acme-carousel'
 
export default function Gallery() {
  let [isOpen, setIsOpen] = useState(false)
 
  return (
    <div>
      <button onClick={() => setIsOpen(true)}>View pictures</button>
 
      {/* Works, since Carousel is used within a Client Component */}
      {isOpen && <Carousel />}
    </div>
  )
}

However, if you try to use it directly within a Server Component, you'll see an error:
app/page.tsx

import { Carousel } from 'acme-carousel'
 
export default function Page() {
  return (
    <div>
      <p>View pictures</p>
 
      {/* Error: `useState` can not be used within Server Components */}
      <Carousel />
    </div>
  )
}

This is because Next.js doesn't know <Carousel /> is using client-only features.

To fix this, you can wrap third-party components that rely on client-only features in your own Client Components:
app/carousel.tsx

'use client'
 
import { Carousel } from 'acme-carousel'
 
export default Carousel

Now, you can use <Carousel /> directly within a Server Component:
app/page.tsx

import Carousel from './carousel'
 
export default function Page() {
  return (
    <div>
      <p>View pictures</p>
 
      {/*  Works, since Carousel is a Client Component */}
      <Carousel />
    </div>
  )
}

We don't expect you to need to wrap most third-party components since it's likely you'll be using them within Client Components. However, one exception is providers, since they rely on React state and context, and are typically needed at the root of an application. Learn more about third-party context providers below.
Using Context Providers

Context providers are typically rendered near the root of an application to share global concerns, like the current theme. Since React context

is not supported in Server Components, trying to create a context at the root of your application will cause an error:
app/layout.tsx

import { createContext } from 'react'
 
//  createContext is not supported in Server Components
export const ThemeContext = createContext({})
 
export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <ThemeContext.Provider value="dark">{children}</ThemeContext.Provider>
      </body>
    </html>
  )
}

To fix this, create your context and render its provider inside of a Client Component:
app/theme-provider.tsx

'use client'
 
import { createContext } from 'react'
 
export const ThemeContext = createContext({})
 
export default function ThemeProvider({
  children,
}: {
  children: React.ReactNode
}) {
  return <ThemeContext.Provider value="dark">{children}</ThemeContext.Provider>
}

Your Server Component will now be able to directly render your provider since it's been marked as a Client Component:
app/layout.tsx

import ThemeProvider from './theme-provider'
 
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html>
      <body>
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  )
}

With the provider rendered at the root, all other Client Components throughout your app will be able to consume this context.

    Good to know: You should render providers as deep as possible in the tree – notice how ThemeProvider only wraps {children} instead of the entire <html> document. This makes it easier for Next.js to optimize the static parts of your Server Components.

Advice for Library Authors

In a similar fashion, library authors creating packages to be consumed by other developers can use the "use client" directive to mark client entry points of their package. This allows users of the package to import package components directly into their Server Components without having to create a wrapping boundary.

You can optimize your package by using 'use client' deeper in the tree, allowing the imported modules to be part of the Server Component module graph.

It's worth noting some bundlers might strip out "use client" directives. You can find an example of how to configure esbuild to include the "use client" directive in the React Wrap Balancer
and Vercel Analytics

repositories.
Client Components
Moving Client Components Down the Tree

To reduce the Client JavaScript bundle size, we recommend moving Client Components down your component tree.

For example, you may have a Layout that has static elements (e.g. logo, links, etc) and an interactive search bar that uses state.

Instead of making the whole layout a Client Component, move the interactive logic to a Client Component (e.g. <SearchBar />) and keep your layout as a Server Component. This means you don't have to send all the component Javascript of the layout to the client.
app/layout.tsx

// SearchBar is a Client Component
import SearchBar from './searchbar'
// Logo is a Server Component
import Logo from './logo'
 
// Layout is a Server Component by default
export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <nav>
        <Logo />
        <SearchBar />
      </nav>
      <main>{children}</main>
    </>
  )
}

Passing props from Server to Client Components (Serialization)

If you fetch data in a Server Component, you may want to pass data down as props to Client Components. Props passed from the Server to Client Components need to be serializable

by React.

If your Client Components depend on data that is not serializable, you can fetch data on the client with a third party library or on the server via a Route Handler.
Interleaving Server and Client Components

When interleaving Client and Server Components, it may be helpful to visualize your UI as a tree of components. Starting with the root layout, which is a Server Component, you can then render certain subtrees of components on the client by adding the "use client" directive.

Within those client subtrees, you can still nest Server Components or call Server Actions, however there are some things to keep in mind:

    During a request-response lifecycle, your code moves from the server to the client. If you need to access data or resources on the server while on the client, you'll be making a new request to the server - not switching back and forth.
    When a new request is made to the server, all Server Components are rendered first, including those nested inside Client Components. The rendered result (RSC Payload) will contain references to the locations of Client Components. Then, on the client, React uses the RSC Payload to reconcile Server and Client Components into a single tree.

    Since Client Components are rendered after Server Components, you cannot import a Server Component into a Client Component module (since it would require a new request back to the server). Instead, you can pass a Server Component as props to a Client Component. See the unsupported pattern and supported pattern sections below.

Unsupported Pattern: Importing Server Components into Client Components

The following pattern is not supported. You cannot import a Server Component into a Client Component:
app/client-component.tsx

'use client'
 
// You cannot import a Server Component into a Client Component.
import ServerComponent from './Server-Component'
 
export default function ClientComponent({
  children,
}: {
  children: React.ReactNode
}) {
  const [count, setCount] = useState(0)
 
  return (
    <>
      <button onClick={() => setCount(count + 1)}>{count}</button>
 
      <ServerComponent />
    </>
  )
}

Supported Pattern: Passing Server Components to Client Components as Props

The following pattern is supported. You can pass Server Components as a prop to a Client Component.

A common pattern is to use the React children prop to create a "slot" in your Client Component.

In the example below, <ClientComponent> accepts a children prop:
app/client-component.tsx

'use client'
 
import { useState } from 'react'
 
export default function ClientComponent({
  children,
}: {
  children: React.ReactNode
}) {
  const [count, setCount] = useState(0)
 
  return (
    <>
      <button onClick={() => setCount(count + 1)}>{count}</button>
      {children}
    </>
  )
}

<ClientComponent> doesn't know that children will eventually be filled in by the result of a Server Component. The only responsibility <ClientComponent> has is to decide where children will eventually be placed.

In a parent Server Component, you can import both the <ClientComponent> and <ServerComponent> and pass <ServerComponent> as a child of <ClientComponent>:
app/page.tsx

// This pattern works:
// You can pass a Server Component as a child or prop of a
// Client Component.
import ClientComponent from './client-component'
import ServerComponent from './server-component'
 
// Pages in Next.js are Server Components by default
export default function Page() {
  return (
    <ClientComponent>
      <ServerComponent />
    </ClientComponent>
  )
}

With this approach, <ClientComponent> and <ServerComponent> are decoupled and can be rendered independently. In this case, the child <ServerComponent> can be rendered on the server, well before <ClientComponent> is rendered on the client.

# Guidelines for using the Supabase library #

const { data: insertData, error: insertError } = await supabase
  .from('table_name')
  .insert([
    { column1: 'value1', column2: 'value2' }
  ]);

Update Data

const { data: updateData, error: updateError } = await supabase
  .from('table_name')
  .update({ column1: 'new_value' })
  .eq('id', 1);

Delete Data

const { data: deleteData, error: deleteError } = await supabase
  .from('table_name')
  .delete()
  .match({ column1: 'value_to_delete' });

Retrieve Specific Columns

const { data: specificColumnsData, error: specificColumnsError } = await supabase
  .from('table_name')
  .select('column1, column2');

Filtering Rows

const { data: filteredData, error: filteredError } = await supabase
  .from('table_name')
  .select('*')
  .eq('column_name', 'value');

Ordering Results


const { data: orderedData, error: orderedError } = await supabase
  .from('table_name')
  .select('*')
  .order('column_name', { ascending: false });

Limiting Results

const { data: limitedData, error: limitedError } = await supabase
  .from('table_name')
  .select('*')
  .limit(10);

Joining Tables

const { data: joinedData, error: joinedError } = await supabase
  .from('table_name')
  .select(`
    column_name,
    other_table_name(column_of_other_table)
  `)
  .eq('other_table_name.foreign_key', 'table_name.primary_key');

Getting the current user

const { data: { user } } = await supabase.auth.getUser()

# UI Component Library #

Here are the locations of the components for you to read the source code before you use them.

Component: Accordion | Path: /components/ui/accordion.tsx       
Component: Alert | Path: /components/ui/alert.tsx
Component: Alert Dialog | Path: /components/ui/alert-dialog.tsx
Component: Aspect Ratio | Path: /components/ui/aspect-ratio.tsx
Component: Avatar | Path: /components/ui/avatar.tsx
Component: Badge | Path: /components/ui/badge.tsx
Component: Breadcrumb | Path: /components/ui/breadcrumb.tsx
Component: Button | Path: /components/ui/button.tsx
Component: Calendar | Path: /components/ui/calendar.tsx
Component: Card | Path: /components/ui/card.tsx
Component: Carousel | Path: /components/ui/carousel.tsx
Component: Checkbox | Path: /components/ui/checkbox.tsx
Component: Collapsible | Path: /components/ui/collapsible.tsx
Component: Command | Path: /components/ui/command.tsx
Component: Context Menu | Path: /components/ui/context-menu.tsx
Component: Dialog | Path: /components/ui/dialog.tsx
Component: Drawer | Path: /components/ui/drawer.tsx
Component: Dropdown Menu | Path: /components/ui/dropdown-menu.tsx
Component: Form | Path: /components/ui/form.tsx
Component: Hover Card | Path: /components/ui/hover-card.tsx
Component: Input | Path: /components/ui/input.tsx
Component: Input OTP | Path: /components/ui/input-otp.tsx
Component: Label | Path: /components/ui/label.tsx
Component: Menubar | Path: /components/ui/menubar.tsx
Component: Navigation Menu | Path: /components/ui/navigation-menu.tsx
Component: Pagination | Path: /components/ui/pagination.tsx
Component: Popover | Path: /components/ui/popover.tsx
Component: Progress | Path: /components/ui/progress.tsx
Component: Radio Group | Path: /components/ui/radio-group.tsx
Component: Resizable | Path: /components/ui/resizable.tsx
Component: Scroll Area | Path: /components/ui/scroll-area.tsx
Component: Select | Path: /components/ui/select.tsx
Component: Separator | Path: /components/ui/separator.tsx
Component: Sheet | Path: /components/ui/sheet.tsx
Component: Skeleton | Path: /components/ui/skeleton.tsx
Component: Slider | Path: /components/ui/slider.tsx
Component: Sonner | Path: /components/ui/sonner.tsx
Component: Switch | Path: /components/ui/siwtch.tsx
Component: Table | Path: /components/ui/table.tsx
Component: Tabs | Path: /components/ui/tabs.tsx
Component: Textarea | Path: /components/ui/textarea.tsx
Component: Toaster | Path: /components/ui/toaster.tsx
Component: Toast | Path: /components/ui/toast.tsx
Component: ToggleGroup | Path: /components/ui/toggle-group.tsx
Component: Toggle | Path: /components/ui/toggle.tsx
Component: Tooltip| Path: /components/ui/tooltip.tsx


## Overall design concerns ##

Remember, you are using Typescript. 
Always be aware of the fact that the difference between server components and client components.
You should always strive to do any data fetching, updating or inserting in server components if you can.
For the most part, the pre-built UI components in /components/ui are client components, so they will most likely need to be imported and interleaved as part of the server component for a given page.


