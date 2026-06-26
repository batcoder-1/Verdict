import { useState } from "react";
import { useAuth } from "../../hooks/useAuth";
import { updateProfile } from "../../api/user";
import { toast } from "sonner";

import Card from "../common/Card";
import Button from "../common/Button";

const ProfileForm = () => {
  const { user, setCurrentUser } = useAuth();

  const [leetcodeHandle, setLeetcodeHandle] = useState(
    user?.leetcode_handle ?? ""
  );

  const [codeforcesHandle, setCodeforcesHandle] = useState(
    user?.codeforces_handle ?? ""
  );

  const [saving, setSaving] = useState(false);

  const hasChanges =
    leetcodeHandle !== (user?.leetcode_handle ?? "") ||
    codeforcesHandle !== (user?.codeforces_handle ?? "");

  const handleSave = async () => {
    try {
      setSaving(true);

      const updatedUser = await updateProfile({
        leetcode_handle: leetcodeHandle || undefined,
        codeforces_handle: codeforcesHandle || undefined,
      });

      setCurrentUser(updatedUser);

      toast.success("Profile updated successfully!");
    } catch {
      toast.error("Failed to update profile.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <Card className="w-full">
      <div className="mb-6 border-b border-zinc-800 pb-4">
        <h2 className="text-2xl font-semibold">
          Profile Settings
        </h2>

        <p className="mt-1 text-sm text-zinc-400">
          Update your competitive programming handles.
        </p>
      </div>

      <div className="space-y-6">
        <div>
          <label className="mb-2 block text-sm font-medium">
            Username
          </label>

          <input
            type="text"
            value={user?.username ?? ""}
            disabled
            className="w-full rounded-lg border border-zinc-700 bg-zinc-800 p-3 text-zinc-400"
          />
        </div>

        <div>
          <label className="mb-2 block text-sm font-medium">
            LeetCode Handle
          </label>

          <input
            type="text"
            value={leetcodeHandle}
            onChange={(e) => setLeetcodeHandle(e.target.value)}
            placeholder="Enter LeetCode Handle"
            className="w-full rounded-lg border border-zinc-700 bg-zinc-800 p-3 outline-none focus:border-blue-500"
          />
        </div>

        <div>
          <label className="mb-2 block text-sm font-medium">
            Codeforces Handle
          </label>

          <input
            type="text"
            value={codeforcesHandle}
            onChange={(e) => setCodeforcesHandle(e.target.value)}
            placeholder="Enter Codeforces Handle"
            className="w-full rounded-lg border border-zinc-700 bg-zinc-800 p-3 outline-none focus:border-blue-500"
          />
        </div>

        <div className="flex justify-end">
          <Button
            onClick={handleSave}
            disabled={saving || !hasChanges}
          >
            {saving ? "Saving..." : "Save Changes"}
          </Button>
        </div>
      </div>
    </Card>
  );
};

export default ProfileForm;