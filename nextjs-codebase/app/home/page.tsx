import { createClient } from "@/utils/supabase/server";
import { redirect } from "next/navigation";

export default async function ProtectedPage() {

  const supabase = createClient();
  const { data } = await supabase.auth.getSession();

  console.log(data.session);

  if (!data.session) {
    redirect("/login?message=Could not authenticate user");
  }
  
  return (
    <>
      <div>Hello</div>
    </>
  );
}
