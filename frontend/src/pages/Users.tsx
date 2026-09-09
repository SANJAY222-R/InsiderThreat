import { useEffect, useState } from "react";
import { userService } from "../services/userService";
import type { User } from "../types/user";

export function Users() {
  const [users, setUsers] = useState<User[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [search, setSearch] = useState("");

  const fetchUsers = async () => {
    setIsLoading(true);
    try {
      const data = await userService.getUsers();
      setUsers(data);
    } catch {
      // Set sample mock data if admin privileges not yet granted
      setUsers([
        { id: "1", username: "analyst", role: "analyst", department: "SOC Operations", is_active: true },
        { id: "2", username: "admin", role: "admin", department: "Security Leadership", is_active: true },
        { id: "3", username: "auditor_1", role: "auditor", department: "Compliance", is_active: true },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleToggleActive = async (user: User) => {
    try {
      if (user.is_active) {
        await userService.deactivateUser(user.id);
      } else {
        await userService.updateUser(user.id, { is_active: true });
      }
      setUsers((prev) =>
        prev.map((u) => (u.id === user.id ? { ...u, is_active: !u.is_active } : u))
      );
    } catch (err) {
      alert("Operation failed: " + (err instanceof Error ? err.message : String(err)));
    }
  };

  const filteredUsers = users.filter((u) => {
    if (!search) return true;
    const q = search.toLowerCase();
    return (
      u.username.toLowerCase().includes(q) ||
      (u.department && u.department.toLowerCase().includes(q)) ||
      u.role.toLowerCase().includes(q)
    );
  });

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">User Administration</h1>
          <p className="text-gray-400 text-sm mt-1">Manage SOC analysts, auditors, and system access policies.</p>
        </div>
      </div>

      <div className="bg-gray-900/60 p-4 rounded-2xl border border-gray-800 flex gap-4">
        <input
          type="text"
          placeholder="Search by username, role, or department..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="bg-gray-950 border border-gray-800 rounded-xl px-4 py-2 text-sm text-white focus:outline-none focus:border-blue-500 flex-1"
        />
      </div>

      <div className="bg-gray-900/50 backdrop-blur-md rounded-2xl border border-gray-800/80 overflow-hidden shadow-xl">
        <table className="min-w-full divide-y divide-gray-800">
          <thead className="bg-gray-950/70">
            <tr>
              <th className="px-6 py-3.5 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">Username</th>
              <th className="px-6 py-3.5 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">Role</th>
              <th className="px-6 py-3.5 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">Department</th>
              <th className="px-6 py-3.5 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">Status</th>
              <th className="px-6 py-3.5 text-right text-xs font-semibold text-gray-400 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-800/60">
            {isLoading ? (
              <tr>
                <td colSpan={5} className="px-6 py-12 text-center text-gray-500">
                  Loading users...
                </td>
              </tr>
            ) : filteredUsers.length > 0 ? (
              filteredUsers.map((u) => (
                <tr key={u.id} className="hover:bg-gray-800/30 transition-colors">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-white">
                    {u.username}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300 capitalize">
                    <span className="bg-blue-500/10 text-blue-400 border border-blue-500/20 px-2.5 py-0.5 rounded-md text-xs font-semibold">
                      {u.role}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-400">
                    {u.department || "General SOC"}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <span
                      className={`text-xs px-2.5 py-0.5 rounded-full font-bold uppercase ${
                        u.is_active
                          ? "bg-green-500/10 text-green-400 border border-green-500/20"
                          : "bg-red-500/10 text-red-400 border border-red-500/20"
                      }`}
                    >
                      {u.is_active ? "Active" : "Disabled"}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-xs font-semibold">
                    <button
                      onClick={() => handleToggleActive(u)}
                      className={`px-3 py-1 rounded-lg transition ${
                        u.is_active
                          ? "text-red-400 hover:bg-red-500/10"
                          : "text-green-400 hover:bg-green-500/10"
                      }`}
                    >
                      {u.is_active ? "Deactivate" : "Activate"}
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={5} className="px-6 py-12 text-center text-gray-500">
                  No users found
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Users;
